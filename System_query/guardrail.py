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
            template="""Task: Classify the user question for an SAP O2C (Order-to-Cash) Graph Database.
User Question: {question}

The graph contains data about:
- SalesOrders, Customers, Products, DeliveryDocuments, BillingDocuments.
- Relationships matching these entities (e.g., PLACED_BY, HAS_ITEM, FULFILLS).

Classification Rules:
1. IN_DOMAIN: Questions about orders, customers, products, shipping/deliveries, or billing within this dataset.
2. OUT_OF_DOMAIN: General knowledge, creative writing, coding help, math, or anything unrelated to this specific business dataset.

Instructions:
- If the question is IN_DOMAIN, return: ALLOWED
- If the question is OUT_OF_DOMAIN, return: REJECTED | <reason why it is not part of this dataset>

Response (Allowed or Rejected | Reason):"""
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
