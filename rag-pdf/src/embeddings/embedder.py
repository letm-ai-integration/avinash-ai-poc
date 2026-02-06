from sentence_transformers import SentenceTransformer
import numpy as np
from src.config.settings import EMBEDDING_MODEL

embedder = SentenceTransformer(EMBEDDING_MODEL)

def create_embeddings(chunks):
    embeddings = embedder.encode(chunks, show_progress_bar=True)
    print(f"Created embeddings for {len(chunks)} chunks.")
    return np.array(embeddings)
