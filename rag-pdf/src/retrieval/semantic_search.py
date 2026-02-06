from sentence_transformers import SentenceTransformer
from src.config.settings import EMBEDDING_MODEL, TOP_K

embedder = SentenceTransformer(EMBEDDING_MODEL)

def semantic_search(query, index, chunks):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, TOP_K)
    print(f"Semantic search for query '{query}' returned top {TOP_K} results.")
    return [chunks[i] for i in indices[0]]
