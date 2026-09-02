from text_extractor import TextExtractor
from table_extractor import TableExtractor
from image_extractor import ImageExtractor

from pathlib import Path


class DocumentParser:

    def __init__(self):

        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
        self.image_extractor = ImageExtractor()

    def parse_pdf(self, pdf_path):

        import json

        pdf_path = Path(pdf_path)

        print(f"Processing PDF: {pdf_path.name}")

        # Extract Text
        text_data = self.text_extractor.extract_text(pdf_path)

        with open(
            f"data/extracted/text/{pdf_path.stem}.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(text_data, f, indent=4)

        # Extract Tables
        table_data = self.table_extractor.extract_tables(pdf_path)

        with open(
            f"data/extracted/tables/{pdf_path.stem}.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(table_data, f, indent=4)

        # Extract Images
        image_data = self.image_extractor.extract_images(
            pdf_path,
            f"data/extracted/images/{pdf_path.stem}"
        )

        # Metadata
        metadata = {
            "pdf_name": pdf_path.name,
            "total_pages": len(text_data),
            "tables_found": len(table_data),
            "images_found": len(image_data)
        }

        with open(
            f"data/extracted/metadata/{pdf_path.stem}.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(metadata, f, indent=4)

        return metadata

if __name__ == "__main__":

    parser = DocumentParser()

    pdf_folder = Path("data/raw_pdfs")

    pdf_files = pdf_folder.glob("*.pdf")

    for pdf_file in pdf_files:

        result = parser.parse_pdf(pdf_file)

        print(result)
