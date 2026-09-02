import json
from pathlib import Path
import ollama


CHUNKS_DIR = Path(
    "data/processing/chunks"
)

OUTPUT_DIR = Path(
    "data/graphrag/document_summaries"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def summarize_document(
    chunk_file
):

    with open(
        chunk_file,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    text = "\n\n".join(
        chunk["text"]
        for chunk in chunks[:20]
    )

    prompt = f"""
Summarize the following research paper.

Include:

1. Main topic
2. Key contributions
3. Important methods
4. Important findings

Paper Content:

{text}
"""

    response = ollama.chat(
        model="phi4-mini:3.8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":

    for file in CHUNKS_DIR.glob(
        "*.json"
    ):

        print(
            f"Processing {file.name}"
        )

        summary = summarize_document(
            file
        )

        output_file = (
            OUTPUT_DIR
            /
            file.name.replace(
                ".json",
                "_summary.txt"
            )
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(summary)

        print(
            f"Saved {output_file.name}"
        )