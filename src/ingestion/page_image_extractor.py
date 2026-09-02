import fitz
import os


class PageImageExtractor:

    def extract_pages(
        self,
        pdf_path,
        output_folder
    ):

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        doc = fitz.open(pdf_path)

        extracted_pages = []

        for page_num in range(len(doc)):

            page = doc[page_num]

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            image_name = (
                f"page_{page_num + 1}.png"
            )

            image_path = os.path.join(
                output_folder,
                image_name
            )

            pix.save(image_path)

            extracted_pages.append(
                {
                    "page_number":
                        page_num + 1,
                    "image_name":
                        image_name,
                    "image_path":
                        image_path
                }
            )

        doc.close()

        return extracted_pages

if __name__ == "__main__":

    extractor = PageImageExtractor()

    pdf_folder = "data/raw_pdfs"
    output_root = "data/extracted/page_images"

    for pdf_file in os.listdir(pdf_folder):

        if pdf_file.endswith(".pdf"):

            pdf_path = os.path.join(
                pdf_folder,
                pdf_file
            )

            report_name = os.path.splitext(
                pdf_file
            )[0]

            output_folder = os.path.join(
                output_root,
                report_name
            )

            extractor.extract_pages(
                pdf_path,
                output_folder
            )

            print(
                f"{report_name}: "
                f"page images generated"
            )