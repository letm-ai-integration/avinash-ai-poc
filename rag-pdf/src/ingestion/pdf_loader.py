from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    print(f"Loaded PDF with {len(reader.pages)} pages.")
    return text
