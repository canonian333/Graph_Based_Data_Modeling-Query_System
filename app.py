from flask import Flask, render_template, request, jsonify
from db import run_query, close_db
from System_query.guardrail import QueryGuardrail
from langchain_neo4j import Neo4jGraph
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, GROQ_API
import os

app = Flask(__name__)

# -----------------------------
# Initialize NLQ Chain
# -----------------------------
if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, GROQ_API]):
    print("WARNING: Missing required environment variables. Some features may not work.")

graph = None
try:
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    # Refresh schema to ensure latest metadata
    graph.refresh_schema()
except Exception as e:
    print(f"Error initializing Neo4jGraph: {e}")

CYPHER_GENERATION_TEMPLATE = """Task: Generate a Cypher query for a Neo4j graph database based on the user question.
You are an expert Cypher developer.

Graph Schema:
Nodes:
- SalesOrder {{id, salesOrder, soldToParty}}
- SalesOrderItem {{id, composite_id, salesOrder, salesOrderItem, material}}
- DeliveryDocument {{id, deliveryDocument}}
- DeliveryItem {{id, composite_id, deliveryDocument, deliveryDocumentItem, referenceSdDocument}}
- BillingDocument {{id, billingDocument, soldToParty, accountingDocument}}
- BillingDocumentItem {{id, composite_id, billingDocument, billingDocumentItem, referenceSdDocument}}
- Customer {{id, customer}}
- Product {{id, product}}

Relationships:
- (SalesOrder)-[:PLACED_BY]->(Customer)
- (SalesOrder)-[:HAS_ITEM]->(SalesOrderItem)
- (SalesOrderItem)-[:REQUESTS_PRODUCT]->(Product)
- (DeliveryItem)-[:FULFILLS_SALES_ORDER]->(SalesOrder)
- (DeliveryDocument)-[:HAS_ITEM]->(DeliveryItem)
- (BillingDocumentItem)-[:REFERENCES_DELIVERY]->(DeliveryDocument)
- (BillingDocument)-[:HAS_ITEM]->(BillingDocumentItem)
- (BillingDocument)-[:BILLS_CUSTOMER]->(Customer)
- (BillingDocument)-[:GENERATES_FINANCIAL]->(AccountingDocument)

Instructions:
1. Only return the Cypher query. No preamble, no markdown code blocks.
2. Use the provided schema ONLY.
3. An order is "delivered" if it has a related DeliveryItem via FULFILLS_SALES_ORDER.
4. An order is "billed" if its related DeliveryDocument is referenced by a BillingDocumentItem via REFERENCES_DELIVERY.
5. "delivered but not billed" means a SalesOrder has a DeliveryItem, but its parent DeliveryDocument is NOT referenced by any BillingDocumentItem.
6. Use node property 'id' for exact matches (e.g. SalesOrder {{id: 'SO_101'}}).
7. Use `RETURN DISTINCT` when returning IDs to avoid duplicate rows.

Generated Schema:
{schema}

Examples:
Question: How many Sales Orders are in the system?
Cypher: MATCH (s:SalesOrder) RETURN count(s)

Question: Identify all orders that are delivered but not yet billed.
Cypher: MATCH (so:SalesOrder)<-[:FULFILLS_SALES_ORDER]-(di:DeliveryItem)<-[:HAS_ITEM]-(dd:DeliveryDocument) WHERE NOT (dd)<-[:REFERENCES_DELIVERY]-(:BillingDocumentItem) RETURN DISTINCT so.id

Question: List the IDs of sales orders placed by customer 'C001'
Cypher: MATCH (so:SalesOrder)-[:PLACED_BY]->(c:Customer {{id: 'C001'}}) RETURN DISTINCT so.id

Question: What products are included in Sales Order 'SO_101'?
Cypher: MATCH (so:SalesOrder {{id: 'SO_101'}})-[:HAS_ITEM]->(soi:SalesOrderItem)-[:REQUESTS_PRODUCT]->(p:Product) RETURN DISTINCT p.id

Question: {question}
Cypher Query:"""

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_GENERATION_TEMPLATE
)

QA_TEMPLATE = """Task: Use the provided Graph Results to answer the user question.
Question: {question}
Graph Results: {context}

Instructions:
1. If the Graph Results contain data (even if just one ID or record), use it to answer the question.
2. Be concise and professional.
3. If and only if the Graph Results are strictly an empty list [], say "No matching records were found."

Example:
Question: List the IDs of sales orders placed by customer 'C001'
Graph Results: [{{'so.id': 'SO_101'}}]
Answer: The sales order placed by customer 'C001' is SO_101.

Answer:"""

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=QA_TEMPLATE
)

llm = ChatGroq(api_key=GROQ_API, model="llama-3.3-70b-versatile", temperature=0)

chain = None
if graph:
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=False,
        allow_dangerous_requests=True,
        validate_cypher=True,
        cypher_prompt=CYPHER_PROMPT,
        qa_prompt=QA_PROMPT,
        return_intermediate_steps=True
    )


@app.route('/')
def index():
    return render_template('index.html')

guardrail = QueryGuardrail()

@app.route('/api/query', methods=['POST'])
def query_graph():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Check guardrail
    check = guardrail.check_query(question)
    if not check['is_allowed']:
        return jsonify({
            "question": question,
            "error": "Query Rejected",
            "answer": check['reason'],
            "cypher": "N/A",
            "results": []
        })
    
    if not chain:
        return jsonify({"error": "NLQ chain not initialized. Check environment variables."}), 500

    try:
        response = chain.invoke({"query": question})
        
        # Extract intermediate steps
        cypher_query = ""
        graph_results = []
        if "intermediate_steps" in response:
            steps = response["intermediate_steps"]
            if len(steps) > 0 and "query" in steps[0]:
                cypher_query = steps[0]["query"]
            if len(steps) > 1 and "context" in steps[1]:
                graph_results = steps[1]["context"]
        
        print(f"DEBUG: Chain Response: {response}")
        
        return jsonify({
            "question": question,
            "cypher": cypher_query,
            "results": graph_results,
            "answer": response.get("result", "I don't know the answer.")
        })
    except Exception as e:
        print(f"Error in /api/query: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/init')
def init_graph():
    # Focused seed query: Get first 10 SalesOrders and their immediate neighbors
    query = """
    MATCH (n:SalesOrder)
    WITH n LIMIT 10
    MATCH (n)-[r]-(m)
    RETURN elementId(n) AS n_id, n, labels(n) AS n_labels, elementId(r) AS r_id, type(r) AS r_type, elementId(m) AS m_id, m, labels(m) AS m_labels
    LIMIT 30
    """
    try:
        results = run_query(query)
        nodes = []
        edges = []
        node_ids = set()

        for r in results:
            n_id = r["n_id"]
            m_id = r["m_id"]
            
            if n_id not in node_ids:
                n_type = r["n_labels"][0] if r["n_labels"] else "Node"
                nodes.append({"data": {"id": n_id, "label": r["n"].get("id") or n_id, "type": n_type, "properties": r["n"]}})
                node_ids.add(n_id)
                
            if m_id not in node_ids:
                m_type = r["m_labels"][0] if r["m_labels"] else "Node"
                nodes.append({"data": {"id": m_id, "label": r["m"].get("id") or m_id, "type": m_type, "properties": r["m"]}})
                node_ids.add(m_id)
                
            edges.append({"data": {
                "id": r["r_id"],
                "source": n_id,
                "target": m_id,
                "label": r["r_type"]
            }})

        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as e:
        print(f"Error in /init: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/search')
def search():
    q = request.args.get('q', '')
    query = """
    MATCH (n)
    WHERE toLower(n.name) CONTAINS toLower($q) OR toLower(n.id) CONTAINS toLower($q)
    RETURN elementId(n) AS id, coalesce(n.name, n.id, "Node") AS label, n AS properties, labels(n)[0] AS type
    """
    try:
        results = run_query(query, {'q': q})
        return jsonify(results)
    except Exception as e:
        print(f"Error in /search: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/neighbors/<node_id>')
def neighbors(node_id):
    depth = request.args.get('depth', 1, type=int)
    # Cap depth at 2 for performance
    depth = min(max(depth, 1), 2)
    
    query = f"""
    MATCH (n)-[r*1..{depth}]-(m)
    WHERE elementId(n) = $id
    UNWIND r AS rel
    RETURN elementId(n) AS n_id, n, labels(n) AS n_labels, 
           elementId(rel) AS r_id, type(rel) AS r_type, 
           elementId(m) AS m_id, m, labels(m) AS m_labels
    LIMIT 100
    """
    try:
        results = run_query(query, {'id': node_id})

        nodes_dict = {}
        edges = []

        for r in results:
            n_id = r["n_id"]
            m_id = r["m_id"]
            
            n_type = r["n_labels"][0] if r["n_labels"] else "Node"
            m_type = r["m_labels"][0] if r["m_labels"] else "Node"
            
            if n_id not in nodes_dict:
                nodes_dict[n_id] = {"data": {"id": n_id, "label": r["n"].get("id") or n_id, "type": n_type, "properties": r["n"]}}
            
            if m_id not in nodes_dict:
                nodes_dict[m_id] = {"data": {"id": m_id, "label": r["m"].get("id") or m_id, "type": m_type, "properties": r["m"]}}
                
            edges.append({"data": {
                "id": r["r_id"],
                "source": n_id,
                "target": m_id,
                "label": r["r_type"]
            }})

        return jsonify({"nodes": list(nodes_dict.values()), "edges": edges})
    except Exception as e:
        print(f"Error in /neighbors/{node_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/nodes_by_ids', methods=['POST'])
def get_nodes_by_ids():
    data = request.json
    ids = data.get('ids', [])
    if not ids:
        return jsonify([])
    
    query = """
    MATCH (n)
    WHERE n.id IN $ids OR elementId(n) IN $ids
    RETURN elementId(n) AS id, coalesce(n.name, n.id, "Node") AS label, n AS properties
    """
    try:
        results = run_query(query, {'ids': ids})
        return jsonify(results)
    except Exception as e:
        print(f"Error in /api/nodes_by_ids: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        print("Starting Flask server on http://127.0.0.1:5000")
        app.run(debug=True, use_reloader=True)
    finally:
        close_db()