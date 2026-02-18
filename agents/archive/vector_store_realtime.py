import faiss
import numpy as np
import pandas as pd

from rag.embedder import embed


# --------------------------------------------------
# Global In-Memory Store (simple + fast)
# --------------------------------------------------

faiss_index = None
product_metadata = None


# --------------------------------------------------
# Index Products
# --------------------------------------------------

def index_products(path="agentic-email-campaign-engine/data/amazon_products_10k.csv"):
    global faiss_index, product_metadata

    df = pd.read_csv(path)

    # Texts used for embedding
    texts = df["description"].fillna("").tolist()

    print("Generating embeddings...")
    embeddings = embed(texts)

    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS Index
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)

    faiss_index.add(embeddings)

    # Store metadata separately
    product_metadata = df.to_dict(orient="records")

    print(f"FAISS index built with {len(product_metadata)} products")


# --------------------------------------------------
# Query Products
# --------------------------------------------------

def query_products(topic, k=10):
    global faiss_index, product_metadata

    if faiss_index is None:
        raise ValueError("FAISS index not initialized. Run index_products() first.")

    query_embedding = embed([topic])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = faiss_index.search(query_embedding, k)

    results = [product_metadata[i] for i in indices[0]]

    return results
