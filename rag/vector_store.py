import faiss
import numpy as np
import pandas as pd
import pickle
import os
import math

from rag.embedder import embed

faiss_index = None
product_metadata = None

default_products_file_name = "products"
# default_products_file_name = "amazon_products_1k"
# default_products_file_name = "fashion"

def index_products_fashion(products_file_name=default_products_file_name):
    global faiss_index, product_metadata

    path = f"agentic-email-campaign-engine/data/{products_file_name}.csv"

    INDEX_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/faiss_index.bin"
    META_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/product_metadata.pkl"

    df = pd.read_csv(path)

    def create_embedding_text(row):
        return (
            f"{row['ProductTitle']}. "
            f"This is a {row['Colour']} {row['ProductType']} for {row['Gender']} "
            f"in the {row['Category']} > {row['SubCategory']} category. "
            f"Best suited for {row['Usage']} wear. "
            f"Product ID: {row['ProductId']}."
        )

    df['text_to_embed'] = df.apply(create_embedding_text, axis=1)

    df.to_csv("output_product.csv", index=False)
    
    texts = (
        df["ProductTitle"].fillna("") + " "
        + df["text_to_embed"].fillna("")
    ).tolist()

    print("Generating embeddings ...")
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


def index_products_amazon_1k(products_file_name='amazon_products_1k'):
    global faiss_index, product_metadata

    path = f"agentic-email-campaign-engine/data/{products_file_name}.csv"

    INDEX_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/faiss_index.bin"
    META_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/product_metadata.pkl"

    df = pd.read_csv(path)

    texts = (
        df["product_name"].fillna("") + " "
        + df["description"].fillna("") + " "
        + df["product_information"].fillna("")
    ).tolist()

    print("Generating embeddings ...")
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


def load_index(products_file_name=default_products_file_name):
    global faiss_index, product_metadata
    
    INDEX_FILE = f"agentic-email-campaign-engine/rag/archive/vdb_{products_file_name}/faiss_index.bin"
    META_FILE = f"agentic-email-campaign-engine/rag/archive/vdb_{products_file_name}/product_metadata.pkl"

    if not os.path.exists(INDEX_FILE):
        raise ValueError("FAISS index file not found. Run index_products() first.")

    print("Loading FAISS index from disk...")

    faiss_index = faiss.read_index(INDEX_FILE)

    with open(META_FILE, "rb") as f:
        product_metadata = pickle.load(f)

    print("FAISS index loaded successfully.")


def query_products(topic, k=10):
    global faiss_index, product_metadata

    if faiss_index is None:
        load_index()

    query_embedding = embed([topic])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = faiss_index.search(query_embedding, k)

    results = [product_metadata[i] for i in indices[0]]
    # print(results)

    return results

if __name__ == "__main__":
    # index_products_fashion('fashion')
    index_products_amazon_1k()

# python agentic-email-campaign-engine\main.py   
# Topic for Campaign:
# winter cloths
# Enter TO EMAIL for campaign:
# pra    