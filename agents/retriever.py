from rag.vector_store import query_products

class RetrieverAgent:

    def run(self, topic: str):
        return query_products(topic, k=10)
