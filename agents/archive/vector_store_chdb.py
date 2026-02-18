import chromadb
import pandas as pd
from rag.embedder import embed

client = chromadb.Client()
collection = client.get_or_create_collection("products")

def index_products(path="agentic-email-campaign-engine/data/products.csv"):

    df = pd.read_csv(path)

    texts = df["description"].tolist()
    embeddings = embed(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=df["product_id"].astype(str).tolist(),
        metadatas=df.to_dict(orient="records")
    )

def query_products(topic, k=10):

    query_embedding = embed([topic])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["metadatas"][0]
