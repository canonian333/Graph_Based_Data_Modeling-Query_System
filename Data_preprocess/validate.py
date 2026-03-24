import os
import sys

report_file = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports\validation.md"

def get_db_credentials():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        import config
        return config.NEO4J_URI or "bolt://localhost:7687", config.NEO4J_USERNAME or "neo4j", config.NEO4J_PASSWORD or "password"
    except ImportError:
        return os.getenv("NEO4J_URI", "bolt://localhost:7687"), os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password")

class GraphValidator:
    def __init__(self, uri, user, password):
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
        
    def clear_flags(self):
        # Clear existing flags to ensure clean state
        with self.driver.session() as session:
            session.run("MATCH (n) REMOVE n:Orphaned, n:Incomplete, n:BrokenFlow, n.validationFlags")

    def check_orphans(self):
        query = """
        MATCH (n) WHERE NOT (n)--()
        SET n:Orphaned, n.validationFlags = coalesce(n.validationFlags, []) + ['OrphanedNode']
        RETURN labels(n)[0] AS label, count(n) AS count
        """
        results = {}
        with self.driver.session() as session:
            res = session.run(query)
            for record in res:
                results[record['label']] = record['count']
        return results

    def check_missing_relationships(self):
        checks = {
            "SalesOrder_Missing_Items": """
                MATCH (s:SalesOrder) WHERE NOT (s)-[:HAS_ITEM]->(:SalesOrderItem)
                SET s:Incomplete, s.validationFlags = coalesce(s.validationFlags, []) + ['MissingItems']
                RETURN count(s) AS count
            """,
            "SalesOrderItem_Missing_Product": """
                MATCH (si:SalesOrderItem) WHERE NOT (si)-[:REQUESTS_PRODUCT]->(:Product)
                SET si:Incomplete, si.validationFlags = coalesce(si.validationFlags, []) + ['MissingProduct']
                RETURN count(si) AS count
            """,
            "DeliveryItem_Missing_Plant": """
                MATCH (di:DeliveryItem) WHERE NOT (di)-[:SHIPPED_FROM_PLANT]->(:Plant)
                SET di:Incomplete, di.validationFlags = coalesce(di.validationFlags, []) + ['MissingPlant']
                RETURN count(di) AS count
            """,
            "BillingDoc_Missing_Customer": """
                MATCH (b:BillingDocument) WHERE NOT (b)-[:BILLS_CUSTOMER]->(:Customer)
                SET b:Incomplete, b.validationFlags = coalesce(b.validationFlags, []) + ['MissingCustomer']
                RETURN count(b) AS count
            """
        }
        results = {}
        with self.driver.session() as session:
            for name, q in checks.items():
                res = session.run(q).single()['count']
                results[name] = res
        return results

    def check_broken_flows(self):
        checks = {
            "Ordered_Not_Shipped": """
                MATCH (so:SalesOrder) WHERE NOT (:DeliveryItem)-[:FULFILLS_SALES_ORDER]->(so)
                SET so:BrokenFlow, so.validationFlags = coalesce(so.validationFlags, []) + ['NotShipped']
                RETURN count(so) AS count
            """,
            "Shipped_Not_Billed": """
                MATCH (di:DeliveryItem) WHERE NOT (di)<-[:REFERENCES_DELIVERY]-(:BillingDocumentItem)
                SET di:BrokenFlow, di.validationFlags = coalesce(di.validationFlags, []) + ['NotBilled']
                RETURN count(di) AS count
            """,
            "Billed_No_Accounting": """
                MATCH (b:BillingDocument) WHERE NOT (b)-[:GENERATES_FINANCIAL]->(:AccountingDocument)
                SET b:BrokenFlow, b.validationFlags = coalesce(b.validationFlags, []) + ['NoAccounting']
                RETURN count(b) AS count
            """
        }
        results = {}
        with self.driver.session() as session:
            for name, q in checks.items():
                res = session.run(q).single()['count']
                results[name] = res
        return results

def run_validation():
    try:
        import neo4j
    except ImportError:
        print("neo4j driver not installed. Ensure it's installed to run graph validations.")
        return

    uri, user, pwd = get_db_credentials()
    
    try:
        validator = GraphValidator(uri, user, pwd)
        validator.driver.verify_connectivity()
    except Exception as e:
        print(f"Failed to connect to Neo4j database: {e}")
        return

    print("Clearing old validation flags...")
    validator.clear_flags()
    
    print("Checking for orphaned nodes...")
    orphans = validator.check_orphans()
    
    print("Checking for missing relationships...")
    missing_rels = validator.check_missing_relationships()
    
    print("Checking for broken business flows...")
    broken_flows = validator.check_broken_flows()
    
    validator.close()

    # Generate Report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# O2C Graph Integrity Validation Report\n\n")
        f.write("This report details the operational state of the graph data, flagging any integrity issues, orphaned data, or broken business flows.\n\n")
        
        f.write("## 1. Orphaned Nodes\n")
        f.write("Nodes disconnected from any other entity. Flagged in graph as `:Orphaned`.\n\n")
        f.write("| Node Label | Orphan Count |\n")
        f.write("| :--- | :--- |\n")
        if orphans:
            for label, count in orphans.items():
                f.write(f"| {label} | {count} |\n")
        else:
            f.write("| All Nodes | 0 (All connected) |\n")
        f.write("\n")
        
        f.write("## 2. Missing Key Relationships\n")
        f.write("Entities structurally missing required conceptual edges. Flagged in graph as `:Incomplete`.\n\n")
        f.write("| Structural Flow Check | Missing Count |\n")
        f.write("| :--- | :--- |\n")
        for check, count in missing_rels.items():
            f.write(f"| {check.replace('_', ' ')} | {count} |\n")
        f.write("\n")
        
        f.write("## 3. Broken Business Flows\n")
        f.write("End-to-End O2C process bottlenecks or disjointed transactions. Flagged as `:BrokenFlow`.\n\n")
        f.write("| Business Process Check | Broken Flow Count |\n")
        f.write("| :--- | :--- |\n")
        for check, count in broken_flows.items():
            f.write(f"| {check.replace('_', ' ')} | {count} |\n")
        f.write("\n")

        f.write("## Data Engineering Action\n")
        f.write("Problematic nodes have successfully been annotated as queryable metadata within the graph. You can inspect the flagged entries using the following Cypher queries:\n")
        f.write("```cypher\n")
        f.write("// Find Orphaned Nodes\n")
        f.write("MATCH (n:Orphaned) RETURN labels(n) AS Entity, n.id AS ID, n.validationFlags AS Flags LIMIT 10;\n\n")
        f.write("// Find Incompletable Structure\n")
        f.write("MATCH (n:Incomplete) RETURN labels(n) AS Entity, n.id AS ID, n.validationFlags AS Flags LIMIT 10;\n\n")
        f.write("// Find Broken Business Processes (e.g. Shipped but not billed)\n")
        f.write("MATCH (n:BrokenFlow) RETURN labels(n) AS Entity, n.id AS ID, n.validationFlags AS Flags LIMIT 10;\n")
        f.write("```\n")

if __name__ == "__main__":
    run_validation()
    print(f"Validation complete! Report saved to {report_file}")
