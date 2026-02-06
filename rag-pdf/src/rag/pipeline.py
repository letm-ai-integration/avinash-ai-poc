from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_text_nltk
from src.embeddings.embedder import create_embeddings
from src.vectorstore.faiss_index import create_faiss_index
from src.retrieval.semantic_search import semantic_search
from src.llm.ollama_client import ask_ollama

def rag_pipeline(pdf_path, question):
    text = load_pdf(pdf_path)
    chunks = chunk_text_nltk(text)
    embeddings = create_embeddings(chunks)
    index = create_faiss_index(embeddings)
    retrieved_chunks = semantic_search(question, index, chunks)
    context = "\n\n".join(retrieved_chunks)
    return ask_ollama(context, question)
