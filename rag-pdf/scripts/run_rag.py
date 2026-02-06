import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.rag.pipeline import rag_pipeline


if __name__ == "__main__":
    pdf_path = "data/samplepdf.pdf"
    question = input("Enter your question: ")
    print("---------------------------------------------------------------------------------------")

    answer = rag_pipeline(pdf_path, question)
    print("---------------------------------------------------------------------------------------")
    print("\nAnswer:\n", answer)
