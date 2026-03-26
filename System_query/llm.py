import sys
import os
import io

# Force UTF-8 encoding for standard output to handle emojis etc on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_neo4j import Neo4jGraph
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, GROQ_API


# -----------------------------
# Initialize Neo4j Graph
# -----------------------------
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)

# Refresh schema to ensure latest metadata
graph.refresh_schema()


# -----------------------------
# Define Custom Cypher Prompt
# -----------------------------
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

Generated Schema:
{schema}

Examples:
Question: How many Sales Orders are in the system?
Cypher: MATCH (s:SalesOrder) RETURN count(s)

Question: Identify all orders that are delivered but not yet billed.
Cypher: MATCH (so:SalesOrder)<-[:FULFILLS_SALES_ORDER]-(di:DeliveryItem)<-[:HAS_ITEM]-(dd:DeliveryDocument) WHERE NOT (dd)<-[:REFERENCES_DELIVERY]-(:BillingDocumentItem) RETURN so.id

Question: List the IDs of sales orders placed by customer 'C001'
Cypher: MATCH (so:SalesOrder)-[:PLACED_BY]->(c:Customer {{id: 'C001'}}) RETURN so.id

Question: What products are included in Sales Order 'SO_101'?
Cypher: MATCH (so:SalesOrder {{id: 'SO_101'}})-[:HAS_ITEM]->(soi:SalesOrderItem)-[:REQUESTS_PRODUCT]->(p:Product) RETURN p.id

Question: {question}
Cypher Query:"""

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_GENERATION_TEMPLATE
)


# -----------------------------
# Define Custom QA Prompt
# -----------------------------
CYPHER_QA_TEMPLATE = """Task: Use the provided Graph Results to answer the user question.

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

CYPHER_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=CYPHER_QA_TEMPLATE
)


# -----------------------------
# Initialize LLM (Groq)
# -----------------------------
llm = ChatGroq(
    api_key=GROQ_API,
    model="llama-3.3-70b-versatile",
    temperature=0
)


# -----------------------------
# Initialize Cypher QA Chain
# -----------------------------
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=False,                   # ✅ Set to False to prevent garbled overlapping output
    allow_dangerous_requests=True,
    validate_cypher=True,
    cypher_prompt=CYPHER_PROMPT,
    qa_prompt=CYPHER_QA_PROMPT,
    return_intermediate_steps=True   # ✅ Return steps so we can print them cleanly ourselves
)


# -----------------------------
# Run Query (Interactive)
# -----------------------------
if __name__ == "__main__":
    print("--- Graph-Based Data Modeling Query System ---")
    print("Enter your question in natural language (type 'exit' to quit).")
    print("-" * 50)

    while True:
        try:
            question = input("\nQuestion: ").strip()
            if not question or question.lower() in ('exit', 'quit', 'q'):
                break

            # Use invoke instead of run (deprecated)
            response = chain.invoke({"query": question})
            
            # Print intermediate steps (Cypher) cleanly
            if "intermediate_steps" in response:
                steps = response["intermediate_steps"]
                # First step is usually the Cypher generation
                if len(steps) > 0 and "query" in steps[0]:
                    print("\n> Generated Cypher:")
                    print("-" * 20)
                    print(steps[0]["query"])
                    print("-" * 20)
                    
                # Second step is often the database result
                if len(steps) > 1 and "context" in steps[1]:
                    print("\n> Graph Results:")
                    print("-" * 20)
                    print(steps[1]["context"])
                    print("-" * 20)
            
            print("\nFinal Answer:")
            print("-" * 20)
            print(response["result"])

        except KeyboardInterrupt:
            break
        except Exception as e:
            import traceback
            print(f"\nError occurred: {e}")
            traceback.print_exc()

    print("\nGoodbye!")
