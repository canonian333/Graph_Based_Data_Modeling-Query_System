import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config.config import GROQ_API

class QueryGuardrail:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=GROQ_API,
            model="llama-3.1-8b-instant",
            temperature=0
        )
        self.classifier_prompt = PromptTemplate(
            input_variables=["question"],
            template="""Task: Classify if the user question is related to the SAP Order-to-Cash (O2C) business dataset.

Graph Schema Context:
- Entities: SalesOrders, Customers, Products, DeliveryDocuments, BillingDocuments.
- Key Properties: id, salesOrder, customer, product, deliveryDocument, billingDocument.
- Relationships: PLACED_BY, HAS_ITEM, REQUESTS_PRODUCT, FULFILLS_SALES_ORDER, REFERENCES_DELIVERY.

Classification Rules:
1. ALLOWED (IN_DOMAIN): 
   - Direct questions about any of the entities above.
   - Aggregations (counts, sums, averages) related to these entities.
   - Filters (e.g., "more than 5 orders", "customer C001").
   - Listing or showing entities (e.g., "Show me all products").
   - Comparisons between entities or time-based queries if they mention these entities.
2. REJECTED (OUT_OF_DOMAIN):
   - General knowledge (e.g., "Who is the president?", "Capital of France").
   - Coding help, math problems unrelated to the data, or creative writing.
   - Questions about unrelated datasets or systems.

Examples:
- "How many Sales Orders are in the system?" -> ALLOWED
- "Find customers who have placed more than 5 sales orders" -> ALLOWED
- "Show me all products" -> ALLOWED
- "Who are the top 10 customers by order count?" -> ALLOWED
- "What is the capital of France?" -> REJECTED | General knowledge question.
- "Calculate the square root of 256" -> REJECTED | Math problem unrelated to dataset.
- "Write a python script to sort a list" -> REJECTED | Coding help.

User Question: {question}

Response Format: ALLOWED or REJECTED | <reason>
Response:"""
        )

    def check_query(self, question):
        if not GROQ_API:
             return {"is_allowed": True} # Fallback if API key missing
             
        try:
            formatted_prompt = self.classifier_prompt.format(question=question)
            response = self.llm.invoke(formatted_prompt).content.strip()
            
            if response.startswith("ALLOWED"):
                return {"is_allowed": True}
            else:
                reason = "This query is outside the scope of the SAP O2C dataset."
                if "|" in response:
                    reason = response.split("|")[1].strip()
                return {"is_allowed": False, "reason": reason}
        except Exception as e:
            print(f"Guardrail Error: {e}")
            return {"is_allowed": True} # Default to allow on error to avoid blocking valid users

if __name__ == "__main__":
    guard = QueryGuardrail()
    print(guard.check_query("How many sales orders?"))
    print(guard.check_query("What is the capital of Japan?"))
