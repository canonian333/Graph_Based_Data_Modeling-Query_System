from neo4j import GraphDatabase
from config.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

def connect_db():
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        driver.verify_connectivity()
        print("Connected to Neo4j")
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
        return None
def run_query(query, parameters=None):
    driver = connect_db()
    if driver:
        with driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    else:
        return []

def close_db():
    driver = connect_db()
    if driver:
        driver.close()
        print("Closed connection to Neo4j")