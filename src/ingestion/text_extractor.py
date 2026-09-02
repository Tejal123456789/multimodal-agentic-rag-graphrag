import fitz  # PyMuPDF


class TextExtractor:

    def extract_text(self, pdf_path):

        doc = fitz.open(pdf_path)

        extracted_text = []

        for page_num in range(len(doc)):

            page = doc[page_num]

            extracted_text.append(
                {
                    "page_number": page_num + 1,
                    "text": page.get_text()
                }
            )

        doc.close()

        return extracted_text