import json
from pathlib import Path


class ImageProcessor:

    def __init__(
        self,
        image_dir="data/extracted/images",
        caption_dir="data/processing/captions",
        output_dir="data/processing/image_descriptions"
    ):

        self.image_dir = Path(image_dir)
        self.caption_dir = Path(caption_dir)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def process_document(self, report_folder):

        image_descriptions = []

        image_files = list(
            report_folder.glob("*")
        )

        caption_file = (
            self.caption_dir /
            f"{report_folder.name}_captions.json"
        )

        captions = []

        if caption_file.exists():

            with open(
                caption_file,
                "r",
                encoding="utf-8"
            ) as f:

                captions = json.load(f)

        for image_file in image_files:

            description = (
                f"Image extracted from "
                f"{report_folder.name}"
            )

            image_name = image_file.stem

            try:
                page_number = int(
                    image_name.split("_")[1]
                )
            except Exception:
                page_number = None

            page_captions = []

            for caption in captions:

                if caption.get("page") == page_number:

                    page_captions.append(
                        caption.get(
                            "caption",
                            ""
                        )
                    )

            if page_captions:

                description = " | ".join(
                    page_captions
                )

            image_descriptions.append(
                {
                    "page": page_number,
                    "image_name": image_file.name,
                    "description": description
                }
            )

        output_file = (
            self.output_dir /
            f"{report_folder.name}_images.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                image_descriptions,
                f,
                indent=4
            )

        print(
            f"{report_folder.name}: "
            f"{len(image_descriptions)} image descriptions created"
        )

    def process_all_documents(self):

        for report_folder in self.image_dir.iterdir():

            if report_folder.is_dir():

                self.process_document(
                    report_folder
                )


if __name__ == "__main__":

    processor = ImageProcessor()

    processor.process_all_documents()