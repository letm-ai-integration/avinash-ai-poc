import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from src.config.settings import CHUNK_SIZE, CHUNK_OVERLAP

nltk.download('punkt_tab')

def chunk_text(text):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start = end - CHUNK_OVERLAP

    print(f"Created {len(chunks)} chunks from text of length {len(text)}.")
    return chunks

def chunk_text_nltk(
    text,
    max_tokens=120,      # approx words per chunk
    overlap_tokens=30    # approx overlap in words
):
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_tokens = word_tokenize(sentence)
        token_count = len(sentence_tokens)

        # If adding this sentence exceeds max_tokens, finalize chunk
        if current_length + token_count > max_tokens:
            chunks.append(" ".join(current_chunk))

            # Create overlap using last N tokens
            overlap = current_chunk[-overlap_tokens:] if overlap_tokens else []
            current_chunk = overlap.copy()
            current_length = len(current_chunk)

        current_chunk.append(sentence)
        current_length += token_count

    # Add remaining text
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
