
import PyPDF2


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.

    Args:
        pdf_file: A file path or file-like object.

    Returns:
        str: Extracted text from all readable PDF pages.

    Raises:
        ValueError: If the PDF is invalid, empty, or encrypted.
        RuntimeError: If PDF extraction fails unexpectedly.
    """

    # --------------------------------------------------
    # Validate Input
    # --------------------------------------------------

    if pdf_file is None:
        raise ValueError("No PDF file was provided.")

    text = []

    try:

        # Reset file pointer when using an uploaded file
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)

        # --------------------------------------------------
        # Read PDF
        # --------------------------------------------------

        pdf_reader = PyPDF2.PdfReader(
            pdf_file,
            strict=False
        )

        # Check for encrypted PDF
        if pdf_reader.is_encrypted:

            try:
                decrypt_status = pdf_reader.decrypt("")

                if decrypt_status == 0:
                    raise ValueError(
                        "Password-protected PDFs are not supported."
                    )

            except ValueError:
                raise

            except Exception as error:
                raise ValueError(
                    "Unable to decrypt the uploaded PDF."
                ) from error

        # Check for empty PDF
        if len(pdf_reader.pages) == 0:
            raise ValueError("The uploaded PDF contains no pages.")

        # --------------------------------------------------
        # Extract Text From Pages
        # --------------------------------------------------

        for page_number, page in enumerate(
            pdf_reader.pages,
            start=1
        ):

            try:

                page_text = page.extract_text()

                if page_text and page_text.strip():
                    text.append(page_text.strip())

            except Exception as error:

                print(
                    f"PDF extraction warning on page "
                    f"{page_number}: {error}"
                )

                continue

        # --------------------------------------------------
        # Validate Extracted Content
        # --------------------------------------------------

        extracted_text = "\n\n".join(text)

        if not extracted_text.strip():

            raise ValueError(
                "No readable text was found in the PDF. "
                "The document may contain scanned images "
                "instead of selectable text."
            )

        return extracted_text

    # --------------------------------------------------
    # Error Handling
    # --------------------------------------------------

    except ValueError:
        raise

    except Exception as error:

        print(f"PDF Extraction Error: {error}")

        raise RuntimeError(
            "Unable to extract text from the uploaded PDF."
        ) from error
