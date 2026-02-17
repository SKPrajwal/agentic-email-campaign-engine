import faiss
import numpy as np
import pandas as pd
import pickle
import os

from rag.embedder import embed


# --------------------------------------------------
# Files for persistence
# --------------------------------------------------

INDEX_FILE = "agentic-email-campaign-engine/rag/faiss_index.bin"
META_FILE = "agentic-email-campaign-engine/rag/product_metadata.pkl"

faiss_index = None
product_metadata = None


# --------------------------------------------------
# Build + Save Index (Run only when data changes)
# --------------------------------------------------

def index_products(path="agentic-email-campaign-engine/data/products_10k.csv"):
    global faiss_index, product_metadata

    df = pd.read_csv(path)

    texts = (
        df["name"].fillna("") + " "
        + df["category"].fillna("") + " "
        + df["color"].fillna("") + " "
        + df["brand"].fillna("") + " "
        + df["description"].fillna("")
    ).tolist()

    print("Generating embeddings (ONE TIME)...")
    embeddings = embed(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings)

    product_metadata = df.to_dict(orient="records")

    # 🔥 Save index locally
    faiss.write_index(faiss_index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(product_metadata, f)

    print(f"Index saved locally with {len(product_metadata)} products.")


# --------------------------------------------------
# Load Index From Disk (FAST STARTUP)
# --------------------------------------------------

def load_index():
    global faiss_index, product_metadata

    if not os.path.exists(INDEX_FILE):
        raise ValueError("FAISS index file not found. Run index_products() first.")

    print("Loading FAISS index from disk...")

    faiss_index = faiss.read_index(INDEX_FILE)

    with open(META_FILE, "rb") as f:
        product_metadata = pickle.load(f)

    print("FAISS index loaded successfully.")


# --------------------------------------------------
# Query Products
# --------------------------------------------------

def query_products(topic, k=10):
    global faiss_index, product_metadata

    if faiss_index is None:
        load_index()

    query_embedding = embed([topic])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = faiss_index.search(query_embedding, k)

    results = [product_metadata[i] for i in indices[0]]

    return results

if __name__ == "__main__":
    index_products()