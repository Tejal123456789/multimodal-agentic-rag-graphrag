import json
import re
from pathlib import Path


class CaptionExtractor:

    def __init__(
        self,
        text_dir="data/extracted/text",
        output_dir="data/processing/captions"
    ):
        self.text_dir = Path(text_dir)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.patterns = {
            "figure": (
                r"(Figure\s+\d+[:.]\s+[^\n]+|"
                r"Fig\.\s*\d+[:.]\s+[^\n]+)"
            ),
            "table": (
                r"(Table\s+\d+[:.]\s+[^\n]+|"
                r"TABLE\s+\d+[:.[^\n]\s+[^\n]+  )"
            )
        }

    def extract_captions(self, json_file):

        with open(json_file, "r", encoding="utf-8") as f:
            pages = json.load(f)

        captions = []

        for page in pages:

            page_number = page["page_number"]
            text = page["text"]

            # Figure Captions
            figure_matches = re.findall(
                self.patterns["figure"],
                text,
                flags=re.IGNORECASE
            )

            for match in figure_matches:
                caption = match.strip()

                # Skip very short captions
                if len(caption.split()) < 5:
                    continue

                captions.append(
                    {
                        "page": page_number,
                        "type": "figure",
                        "caption": caption
                    }
                )

            # Table Captions
            table_matches = re.findall(
                self.patterns["table"],
                text,
                flags=re.IGNORECASE
            )

            for match in table_matches:
                captions.append(
                    {
                        "page": page_number,
                        "type": "table",
                        "caption": match.strip()
                    }
                )

        return captions

    def process_all_documents(self):

        json_files = self.text_dir.glob("*.json")

        for json_file in json_files:

            captions = self.extract_captions(
                json_file
            )

            output_file = (
                self.output_dir /
                f"{json_file.stem}_captions.json"
            )

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    captions,
                    f,
                    indent=4
                )

            print(
                f"{json_file.stem}: "
                f"{len(captions)} captions found"
            )


if __name__ == "__main__":

    extractor = CaptionExtractor()

    extractor.process_all_documents()