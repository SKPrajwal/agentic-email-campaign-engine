import faiss
import numpy as np
import pandas as pd
import pickle
import os
import math

from embedder import embed


# --------------------------------------------------
# Files for persistence
# --------------------------------------------------

INDEX_FILE = "agentic-email-campaign-engine/rag/faiss_index.bin"
META_FILE = "agentic-email-campaign-engine/rag/product_metadata.pkl"

faiss_index = None
product_metadata = None

# default_products_file_name = "amazon_products_1k"
default_products_file_name = "fasion"


# --------------------------------------------------    
# Build + Save Index (Run only when data changes)
# --------------------------------------------------

def index_products_new(products_file_name=default_products_file_name):
    global faiss_index, product_metadata
    
    path = f"agentic-email-campaign-engine/data/{products_file_name}.csv"

    # INDEX_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/faiss_index.bin"
    # META_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/product_metadata.pkl"

    df = pd.read_csv(path)
    BATCH_SIZE = 1000

    # texts = (
    #     df["name"].fillna("") + " "
    #     + df["category"].fillna("") + " "
    #     + df["color"].fillna("") + " "
    #     + df["brand"].fillna("") + " "
    #     + df["description"].fillna("")
    # ).tolist() # for 100 products with no images url
    
    texts = (
        df["product_name"].fillna("") + " "
        + df["amazon_category_and_sub_category"].fillna("") + " "
        + df["product_information"].fillna("") + " "
        + df["product_description"].fillna("") + " "
        + df["customer_questions_and_answers"].fillna("") + " "
        + df["description"].fillna("")
    ).tolist()

    print("Generating embeddings ...")

    total_records = len(texts)
    num_batches = math.ceil(total_records / BATCH_SIZE)

    print(f"Total Records: {total_records}")
    print(f"Creating {num_batches} FAISS batch indexes...")

    start_batch_id = 0
    for batch_id in range(start_batch_id, num_batches):

        start = batch_id * BATCH_SIZE
        end = start + BATCH_SIZE

        batch_texts = texts[start:end]
        batch_df = df.iloc[start:end]

        print(f"\nProcessing batch {batch_id+1} ({start} → {end})")

        embeddings = embed(batch_texts)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_index.add(embeddings)

        product_metadata = batch_df.to_dict(orient="records")

        INDEX_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/index/faiss_index.bin"
        META_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/metadata/product_metadata.pkl"

        faiss.write_index(faiss_index, INDEX_FILE)

        with open(META_FILE, "wb") as f:
            pickle.dump(product_metadata, f)

        print(
            f"Saved Batch {batch_id+1} → "
            f"{len(product_metadata)} records"
        )

    print("\n✅ ALL FAISS BATCHES SAVED SUCCESSFULLY")

def index_products(products_file_name=default_products_file_name):
    global faiss_index, product_metadata

    path = f"agentic-email-campaign-engine/data/{products_file_name}.csv"

    INDEX_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/faiss_index.bin"
    META_FILE = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/product_metadata.pkl"

    df = pd.read_csv(path)

    discriber = ProductDescAgent("planner")

    df["ProductDescriptionLLM"] = df.apply(generate_description, axis=1)
    print(df["ProductDescriptionLLM"])
    df.to_csv("output_product.csv", index=False)


    texts = (
    df["Gender"].fillna("") + " "
    + df["SubCategory"].fillna("") + " "
    + df["ProductType"].fillna("") + " "
    + df["ProductTitle"].fillna("") + " "
    + df["ProductDescriptionLLM"].fillna("")
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

# --------------------------------------------------
# Load Index From Disk (FAST STARTUP)
# --------------------------------------------------

def load_index_old(products_file_name=default_products_file_name):
    global faiss_index, product_metadata
    
    INDEX_PATH = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/index"
    META_PATH = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/metadata"

    if not os.path.exists(INDEX_PATH):
        raise ValueError("FAISS index file not found. Run index_products() first.")

    print("Loading FAISS index from disk...")

    faiss_index = faiss.read_index(INDEX_FILE)

    with open(META_FILE, "rb") as f:
        product_metadata = pickle.load(f)

    print("FAISS index loaded successfully.")

import os
import faiss
import pickle

faiss_index = None
product_metadata = []

def load_index(products_file_name=default_products_file_name):
    global faiss_index, product_metadata

    BASE_PATH = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}"
    # INDEX_PATH = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/index"
    # META_PATH = f"agentic-email-campaign-engine/rag/vdb_{products_file_name}/metadata"

    if not os.path.exists(BASE_PATH):
        raise ValueError("Vector DB path not found. Run index_products() first.")

    print("Loading FAISS indexes from disk...")

    indexes = []
    all_metadata = []

    # 🔹 iterate through all subfolders/files
    for root, dirs, files in BASE_PATH:

        INDEX_FILE = os.path.join(root, "index")
        META_FILE = os.path.join(root, "metadata")

        if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):

            print(f"Loading index from: {INDEX_FILE}")

            # Load FAISS index
            idx = faiss.read_index(INDEX_FILE)
            indexes.append(idx)

            # Load metadata
            with open(META_FILE, "rb") as f:
                meta = pickle.load(f)
                all_metadata.extend(meta)

    if not indexes:
        raise ValueError("No FAISS indexes found in the provided path.")

    # 🔥 Merge all indexes into one searchable index
    faiss_index = indexes[0]

    for idx in indexes[1:]:
        faiss_index.merge_from(idx)

    product_metadata = all_metadata

    print(f"FAISS indexes loaded successfully. Total vectors: {faiss_index.ntotal}")


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
    print(results)

    return results

if __name__ == "__main__":
    index_products('fasion')