import json
from pathlib import Path


class PageImageProcessor:

    def __init__(
        self,
        page_image_dir="data/extracted/page_images",
        caption_dir="data/processing/captions",
        output_dir="data/processing/page_image_descriptions"
    ):

        self.page_image_dir = Path(page_image_dir)
        self.caption_dir = Path(caption_dir)

        self.text_dir = Path(
            "data/extracted/text"
        )

        self.output_dir = Path(output_dir)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def process_document(self, report_folder):

        descriptions = []

        caption_file = (
            self.caption_dir /
            f"{report_folder.name}_captions.json"
        )

        captions = []
        page_texts = []

        if caption_file.exists():

            with open(
                caption_file,
                "r",
                encoding="utf-8"
            ) as f:

                captions = json.load(f)

        text_file = (
            self.text_dir /
            f"{report_folder.name}.json"
        )

        if text_file.exists():

            with open(
                text_file,
                "r",
                encoding="utf-8"
            ) as f:

                page_texts = json.load(f)

        for page_image in report_folder.glob("*.png"):

            try:
                page_number = int(
                    page_image.stem.split("_")[1]
                )
            except Exception:
                continue

            page_captions = []

            for caption in captions:

                if caption["page"] == page_number:

                    page_captions.append(
                        caption["caption"]
                    )

            description = " | ".join(
                page_captions
            )

            page_text = ""

            for page_info in page_texts:

                if page_info["page_number"] == page_number:

                    page_text = page_info["text"][:1000]

                    break

            description += (
                "\n\nPage text:\n"
                + page_text
            )

            descriptions.append(
                {
                    "page": page_number,
                    "image_name": page_image.name,
                    "description": description
                }
            )

        output_file = (
            self.output_dir /
            f"{report_folder.name}_pages.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                descriptions,
                f,
                indent=4
            )

        print(
            f"{report_folder.name}: "
            f"{len(descriptions)} descriptions created"
        )

    def process_all_documents(self):

        for report_folder in self.page_image_dir.iterdir():

            if report_folder.is_dir():

                self.process_document(
                    report_folder
                )


if __name__ == "__main__":

    processor = PageImageProcessor()

    processor.process_all_documents()