import os
import json
import logging
import glob

base_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\data\preprocesed_data"
log_file = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports\ingestion.log"

os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

class Neo4jIngester:
    def __init__(self, uri, user, password):
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()

    def create_constraints(self):
        labels = [
            'Customer', 'BusinessPartner', 'CompanyCode', 'GLAccount',
            'Product', 'Plant', 'SalesOrder', 'SalesOrderItem',
            'DeliveryDocument', 'DeliveryItem', 'BillingDocument',
            'BillingDocumentItem', 'AccountingDocument', 'ShippingPoint'
        ]
        with self.driver.session() as session:
            for label in labels:
                query = f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.id IS UNIQUE"
                try:
                    session.run(query)
                    logging.info(f"Ensured constraint/index for Label: {label}")
                except Exception as e:
                    logging.error(f"Failed creating constraint for {label}: {e}")

    def load_nodes(self, label, data, id_field='id'):
        if not data:
            return
        query = f"""
        UNWIND $batch AS row
        MERGE (n:{label} {{id: row.{id_field}}})
        SET n += row
        """
        self._execute_batch(query, data)
        logging.info(f"Loaded {len(data)} nodes of type {label}")

    def load_edges(self, src_label, dst_label, rel_type, edges_data):
        if not edges_data:
            return
        query = f"""
        UNWIND $batch AS row
        MATCH (src:{src_label} {{id: row.src_id}})
        MATCH (dst:{dst_label} {{id: row.dst_id}})
        MERGE (src)-[r:{rel_type}]->(dst)
        """
        self._execute_batch(query, edges_data)
        logging.info(f"Loaded {len(edges_data)} edges of type {rel_type} between {src_label} and {dst_label}")

    def _execute_batch(self, query, data, batch_size=1000):
        with self.driver.session() as session:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                try:
                    session.run(query, batch=batch)
                except Exception as e:
                    logging.error(f"Error in batch execution: {e}")

def get_data(folder_name):
    path = os.path.join(base_dir, folder_name)
    files = glob.glob(os.path.join(path, "*.jsonl"))
    if not files:
        return []
    records = []
    with open(files[0], 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line))
    return records

def ingest_all():
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        import config
        uri = config.NEO4J_URI or "bolt://localhost:7687"
        user = config.NEO4J_USERNAME or "neo4j"
        password = config.NEO4J_PASSWORD or "password"
    except ImportError:
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
    
    try:
        import neo4j
    except ImportError:
        logging.error("neo4j driver not installed. Run `pip install neo4j`")
        print("Please install neo4j driver using: pip install neo4j")
        return

    logging.info(f"Connecting to Neo4j at {uri}...")
    try:
        ingester = Neo4jIngester(uri, user, password)
        ingester.driver.verify_connectivity()
    except Exception as e:
        logging.error(f"Failed to connect to Neo4j. Is it running locally? Error: {e}")
        return

    logging.info("Creating constraints/indexes for high query fields...")
    ingester.create_constraints()

    logging.info("--- Starting Node Ingestion ---")
    
    bp = get_data("business_partners")
    customers = [r for r in bp if r.get('customer') and str(r['customer']) not in ('UNKNOWN', 'None', '')]
    ingester.load_nodes('Customer', customers, id_field='customer')
    
    bps = [r for r in bp if r.get('businessPartner') and str(r['businessPartner']) not in ('UNKNOWN', 'None', '')]
    ingester.load_nodes('BusinessPartner', bps, id_field='businessPartner')
    
    prods = get_data("products")
    ingester.load_nodes('Product', prods, id_field='product')
    
    plants = get_data("plants")
    ingester.load_nodes('Plant', plants, id_field='plant')
    
    so = get_data("sales_order_headers")
    ingester.load_nodes('SalesOrder', so, id_field='salesOrder')
    
    so_items = get_data("sales_order_items")
    for r in so_items:
        r['composite_id'] = f"{r['salesOrder']}_{r['salesOrderItem']}"
    ingester.load_nodes('SalesOrderItem', so_items, id_field='composite_id')
    
    deliv = get_data("outbound_delivery_headers")
    ingester.load_nodes('DeliveryDocument', deliv, id_field='deliveryDocument')
    
    del_items = get_data("outbound_delivery_items")
    for r in del_items:
        r['composite_id'] = f"{r['deliveryDocument']}_{r['deliveryDocumentItem']}"
    ingester.load_nodes('DeliveryItem', del_items, id_field='composite_id')
    
    bill = get_data("billing_document_headers")
    ingester.load_nodes('BillingDocument', bill, id_field='billingDocument')
    
    bill_items = get_data("billing_document_items")
    for r in bill_items:
        r['composite_id'] = f"{r['billingDocument']}_{r['billingDocumentItem']}"
    ingester.load_nodes('BillingDocumentItem', bill_items, id_field='composite_id')
    
    je = get_data("journal_entry_items_accounts_receivable")
    unique_gl = list({r['glAccount'] for r in je if r.get('glAccount')})
    ingester.load_nodes('GLAccount', [{'id': gl} for gl in unique_gl], id_field='id')
    
    unique_comp = list({r['companyCode'] for r in je if r.get('companyCode')})
    ingester.load_nodes('CompanyCode', [{'id': comp} for comp in unique_comp], id_field='id')
    
    acc_docs_dict = {r['accountingDocument']: r for r in je if r.get('accountingDocument')}
    ingester.load_nodes('AccountingDocument', list(acc_docs_dict.values()), id_field='accountingDocument')

    logging.info("--- Starting Edge Ingestion ---")
    
    edges = [{'src_id': r['salesOrder'], 'dst_id': r['soldToParty']} for r in so if r.get('soldToParty')]
    ingester.load_edges('SalesOrder', 'Customer', 'PLACED_BY', edges)
    
    edges = [{'src_id': r['salesOrder'], 'dst_id': r['composite_id']} for r in so_items]
    ingester.load_edges('SalesOrder', 'SalesOrderItem', 'HAS_ITEM', edges)
    
    edges = [{'src_id': r['composite_id'], 'dst_id': r['material']} for r in so_items if r.get('material') and str(r['material']) not in ('UNKNOWN', 'None', 'nan')]
    ingester.load_edges('SalesOrderItem', 'Product', 'REQUESTS_PRODUCT', edges)
    
    edges = [{'src_id': r['composite_id'], 'dst_id': r['referenceSdDocument']} for r in del_items if r.get('referenceSdDocument') and str(r['referenceSdDocument']) not in ('UNKNOWN', 'None', 'nan')]
    ingester.load_edges('DeliveryItem', 'SalesOrder', 'FULFILLS_SALES_ORDER', edges)

    edges = [{'src_id': r['deliveryDocument'], 'dst_id': r['composite_id']} for r in del_items]
    ingester.load_edges('DeliveryDocument', 'DeliveryItem', 'HAS_ITEM', edges)
    
    edges = [{'src_id': r['composite_id'], 'dst_id': r['referenceSdDocument']} for r in bill_items if r.get('referenceSdDocument') and str(r['referenceSdDocument']) not in ('UNKNOWN', 'None', 'nan')]
    ingester.load_edges('BillingDocumentItem', 'DeliveryDocument', 'REFERENCES_DELIVERY', edges)

    edges = [{'src_id': r['billingDocument'], 'dst_id': r['composite_id']} for r in bill_items]
    ingester.load_edges('BillingDocument', 'BillingDocumentItem', 'HAS_ITEM', edges)
    
    edges = [{'src_id': r['billingDocument'], 'dst_id': r['soldToParty']} for r in bill if r.get('soldToParty')]
    ingester.load_edges('BillingDocument', 'Customer', 'BILLS_CUSTOMER', edges)
    
    edges = [{'src_id': r['billingDocument'], 'dst_id': r['accountingDocument']} for r in bill if r.get('accountingDocument') and str(r['accountingDocument']) not in ('UNKNOWN', 'None', 'nan')]
    ingester.load_edges('BillingDocument', 'AccountingDocument', 'GENERATES_FINANCIAL', edges)
    
    edges = [{'src_id': r['accountingDocument'], 'dst_id': r['glAccount']} for r in je if r.get('accountingDocument') and r.get('glAccount')]
    ingester.load_edges('AccountingDocument', 'GLAccount', 'POSTS_TO', edges)
    
    edges = [{'src_id': r['customer'], 'dst_id': r['businessPartner']} for r in bp if r.get('customer') and r.get('businessPartner')]
    ingester.load_edges('Customer', 'BusinessPartner', 'IS', edges)
    
    edges = [{'src_id': r['composite_id'], 'dst_id': r['plant']} for r in del_items if r.get('plant') and str(r['plant']) not in ('UNKNOWN', 'None', 'nan')]
    ingester.load_edges('DeliveryItem', 'Plant', 'SHIPPED_FROM_PLANT', edges)
    
    logging.info("--- Ingestion Complete ---")
    ingester.close()

if __name__ == "__main__":
    ingest_all()
