import fitz

def extract_text_from_pdf(pdf_path: str):

    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    page_count = len(document)

    document.close()

    return{
        "text": full_text,
        "pages": page_count,
        "characters": len(full_text)
    }    

