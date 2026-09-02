import json
from pathlib import Path

import chromadb


class ChromaManager:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="vector_store/chroma_db"
        )

        # Delete old collection if it exists
        try:
            self.client.delete_collection(
                name="multimodal_rag"
            )
            print("Old collection deleted.")
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name="multimodal_rag"
        )

        self.embedding_dir = Path(
            "data/processing/embeddings"
        )

    def load_embeddings(self):

        doc_count = 0

        for json_file in self.embedding_dir.glob("*.json"):

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            for idx, item in enumerate(data):

                if "embedding" not in item:
                    continue

                text = ""

                if "text" in item:
                    text = item["text"]

                elif "summary" in item:
                    text = item["summary"]

                elif "description" in item:
                    text = item["description"]

                elif "caption" in item:
                    text = item["caption"]

                unique_id = (
                    f"{json_file.stem}_{idx}"
                )

                self.collection.add(
                    ids=[unique_id],
                    embeddings=[item["embedding"]],
                    documents=[text],
                    metadatas=[
                        {
                            "source_file": json_file.name,
                            "source": item.get("source", ""),
                            "type": item.get("type", ""),
                            "page": item.get("page", -1)
                        }
                    ]
                )

                doc_count += 1

        print(
            f"{doc_count} records inserted "
            f"into ChromaDB."
        )


if __name__ == "__main__":

    manager = ChromaManager()

    manager.load_embeddings()