import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
class Chunker:

    def __init__(
        self,
        text_dir="data/extracted/text",
        output_dir="data/processing/chunks",
        chunk_size=1000,
        chunk_overlap=200
    ):

        self.text_dir = Path(text_dir)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

    def split_text(self, text):

        return self.text_splitter.split_text(text)

    def process_document(self, json_file):

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as f:

            pages = json.load(f)

        document_chunks = []

        chunk_id = 1

        for page in pages:

            page_number = page["page_number"]
            text = page["text"]

            chunks = self.split_text(text)

            for chunk in chunks:

                document_chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "page": page_number,
                        "text": chunk
                    }
                )

                chunk_id += 1

        output_file = (
            self.output_dir /
            f"{json_file.stem}_chunks.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                document_chunks,
                f,
                indent=4
            )

        print(
            f"{json_file.stem}: "
            f"{len(document_chunks)} chunks created"
        )

    def process_all_documents(self):

        for json_file in self.text_dir.glob("*.json"):

            self.process_document(json_file)


if __name__ == "__main__":

    chunker = Chunker()

    chunker.process_all_documents()