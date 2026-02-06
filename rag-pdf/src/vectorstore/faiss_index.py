import faiss

def create_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    print(f"FAISS index created with {index.ntotal} vectors of dimension {dim}.")
    return index
