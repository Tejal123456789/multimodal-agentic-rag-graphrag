import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.chunk_dir = Path(
            "data/processing/chunks"
        )

        self.table_dir = Path(
            "data/processing/table_summaries"
        )

        self.image_dir = Path(
            "data/processing/image_descriptions"
        )

        self.page_image_dir = Path(
            "data/processing/page_image_descriptions"
        )

        self.caption_dir = Path(
            "data/processing/captions"
        )

        self.output_dir = Path(
            "data/processing/embeddings"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate_embedding(self, text):

        return self.model.encode(
            text
        ).tolist()

    def process_json_file(
        self,
        json_file,
        text_field
    ):

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        embedded_records = []

        for item in data:

            text = item.get(
                text_field,
                ""
            )

            if not text:
                continue

            embedding = self.generate_embedding(
                text
            )

            item["embedding"] = embedding

            # Add source metadata
            item["source"] = json_file.stem
            if "image_name" in item:
                item["type"] = "page_image"

            elif "table" in json_file.stem:
                item["type"] = "table"

            else:
                item["type"] = "text"

            embedded_records.append(item)

        output_file = (
            self.output_dir /
            f"{json_file.stem}_embeddings.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                embedded_records,
                f
            )

        print(
            f"{json_file.name}: "
            f"{len(embedded_records)} embeddings"
        )

    def process_all(self):

        for file in self.chunk_dir.glob("*.json"):
            self.process_json_file(
                file,
                "text"
            )

        for file in self.table_dir.glob("*.json"):
            self.process_json_file(
                file,
                "summary"
            )

        for file in self.image_dir.glob("*.json"):
            self.process_json_file(
                file,
                "description"
            )

        for file in self.page_image_dir.glob("*.json"):
            self.process_json_file(
                file,
                "description"
            )

        for file in self.caption_dir.glob("*.json"):
            self.process_json_file(
                file,
                "caption"
            )


if __name__ == "__main__":

    generator = EmbeddingGenerator()

    generator.process_all()