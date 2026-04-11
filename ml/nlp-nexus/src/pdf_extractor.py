import PyPDF2


def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.

    Args:
        pdf_file: Path to a PDF file or a file object

    Returns:
        str: Extracted text from all pages of the PDF
    """

    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text