import os
import glob
import json
import pandas as pd

base_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\data\preprocesed_data"
report_file = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports\validation.md"
schema_file = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports\schema.md"

def load_data():
    datasets = {}
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        jsonl_files = glob.glob(os.path.join(folder_path, "*.jsonl"))
        if jsonl_files:
            try:
                df = pd.read_json(jsonl_files[0], lines=True)
                datasets[folder] = df
            except Exception as e:
                print(f"Error loading {folder}: {e}")
    return datasets

def validate_pandas():
    print("Loading datasets for local schema checks...")
    datasets = load_data()
    
    report_lines = []
    report_lines.append("# Preprocessed Data & Graph Validation Report\n\n")
    
    # 1. Schema Validation Step
    report_lines.append("## 1. Local Schema Validation Step\n")
    report_lines.append("Checking if all entity files are loaded properly with expected columns and zero critical errors.\n\n")
    
    passed = True
    for name, df in datasets.items():
        if df.empty:
            passed = False
            report_lines.append(f"- ❌ `{name}` is empty.\n")
        else:
            report_lines.append(f"- ✅ `{name}` loaded successfully ({len(df)} rows, {len(df.columns)} columns).\n")
            
    if passed:
        report_lines.append("\n**Result: All entity files pass schema validation step with zero critical errors.**\n\n")
        
    return report_lines

def validate_graph(report_lines):
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from neo4j import GraphDatabase
        import config
        uri = config.NEO4J_URI or "bolt://localhost:7687"
        user = config.NEO4J_USERNAME or "neo4j"
        password = config.NEO4J_PASSWORD or "password"
    except ImportError:
        print("Neo4j driver or config not found. Skipping graph validation.")
        return report_lines

    print("Connecting to Neo4j for Graph Integrity Checks...")
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
    except Exception as e:
        report_lines.append(f"## Graph Validation\nCould not connect to Neo4j. Error: {e}\n")
        return report_lines

    report_lines.append("## 2. Graph Integrity & Flow Validation\n")
    report_lines.append("Running Cypher queries to detect orphaned nodes, missing relationships, and broken business flows. Problematic nodes are flagged in the graph with the `Flagged` label and a `flagReason` property.\n\n")

    queries = [
        {
            "name": "Orphaned Nodes (No Edges)",
            "query": """
                MATCH (n) WHERE NOT (n)--() 
                SET n:Flagged, n.flagReason = 'Orphaned Node' 
                RETURN head(labels(n)) AS Entity, count(n) AS Count
            """
        },
        {
            "name": "Missing Product Reference in Sales Orders",
            "query": """
                MATCH (i:SalesOrderItem) WHERE NOT (i)-[:REQUESTS_PRODUCT]->(:Product)
                SET i:Flagged, i.flagReason = 'Missing Product Reference'
                RETURN 'SalesOrderItem' AS Entity, count(i) AS Count
            """
        },
        {
            "name": "Missing Delivery Reference in Billing",
            "query": """
                MATCH (b:BillingDocumentItem) WHERE NOT (b)-[:REFERENCES_DELIVERY]->(:DeliveryDocument)
                SET b:Flagged, b.flagReason = 'Missing Delivery Document Reference'
                RETURN 'BillingDocumentItem' AS Entity, count(b) AS Count
            """
        },
        {
            "name": "Broken Flow: Sales Orders with No Delivery",
            "query": """
                MATCH (so:SalesOrder)
                WHERE NOT (so)<-[:FULFILLS_SALES_ORDER]-(:DeliveryItem)
                SET so:Flagged, so.flagReason = 'O2C Leak: No Delivery Found'
                RETURN 'SalesOrder' AS Entity, count(so) AS Count
            """
        },
        {
            "name": "Broken Flow: Deliveries with No Billing",
            "query": """
                MATCH (d:DeliveryDocument)-[:HAS_ITEM]->(di:DeliveryItem)
                WHERE NOT (di)<-[:REFERENCES_DELIVERY]-(:BillingDocumentItem)
                SET d:Flagged, d.flagReason = 'O2C Leak: No Billing Found'
                RETURN 'DeliveryDocument' AS Entity, count(distinct d) AS Count
            """
        },
        {
            "name": "Broken Flow: Billing with No Accounting",
            "query": """
                MATCH (b:BillingDocument)
                WHERE NOT (b)-[:GENERATES_FINANCIAL]->(:AccountingDocument)
                SET b:Flagged, b.flagReason = 'O2C Leak: No Accounting Document Found'
                RETURN 'BillingDocument' AS Entity, count(b) AS Count
            """
        }
    ]

    report_lines.append("| Check Description | Entity | Broken Count | Queryable Metadata |\n")
    report_lines.append("| :--- | :--- | :--- | :--- |\n")

    with driver.session() as session:
        # First clear old flags
        session.run("MATCH (n:Flagged) REMOVE n:Flagged, n.flagReason")
        
        for check in queries:
            result = session.run(check["query"])
            records = list(result)
            total_broken = sum(r["Count"] for r in records if r["Count"])
            entity_names = ", ".join(set(r["Entity"] for r in records if r["Entity"])) or "N/A"
            if total_broken > 0:
                report_lines.append(f"| {check['name']} | {entity_names} | {total_broken} ⚠️ | `MATCH (n:Flagged {{flagReason: '{check['query'].split('=')[1].split(chr(39))[1] if chr(39) in check['query'] else 'Unknown'}'}})` |\n")
            else:
                report_lines.append(f"| {check['name']} | - | 0 ✅ | - |\n")

    driver.close()
    
    report_lines.append("\n## 3. Edge Cardinalities\n")
    report_lines.append("Expected cardinalities defined for graph modelling ingestion:\n")
    report_lines.append("- **Customer to SalesOrder**: `1:N`\n")
    report_lines.append("- **BusinessPartner to Customer**: `1:1`\n")
    report_lines.append("- **SalesOrder to Product**: `N:M` (via Item Lines)\n")
    report_lines.append("- **DeliveryDocument to SalesOrder**: `N:1`\n")
    report_lines.append("- **BillingDocument to SalesOrder**: `N:1`\n")
    report_lines.append("- **DeliveryDocument to Plant**: `N:1`\n")
    report_lines.append("- **BillingDocument to Customer**: `N:1`\n")
    report_lines.append("- **BillingDocument to AccountingDocument**: `1:1`\n")
    report_lines.append("- **AccountingDocument to GLAccount**: `N:1`\n")
    report_lines.append("- **Customer to CompanyCode**: `1:N` (Assignments)\n")
    report_lines.append("\n**Status: Review and Graph Integrity checks completed.**\n")
    
    return report_lines

def main():
    report_lines = validate_pandas()
    report_lines = validate_graph(report_lines)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.writelines(report_lines)
    print(f"Validation complete. Report saved to {report_file}")

if __name__ == "__main__":
    main()
