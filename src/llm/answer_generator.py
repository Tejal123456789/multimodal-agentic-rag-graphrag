import sys
from pathlib import Path
import ollama

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker


class AnswerGenerator:

    def __init__(self):

        self.retriever = HybridRetriever()
        self.reranker = Reranker()

    def generate_answer(
        self,
        query,
        top_k=5
    ):

        results = self.retriever.retrieve(
            query,
            top_k=20
        )

        documents = results["documents"]
        metadatas = results["metadatas"]

        documents = self.reranker.rerank(
            query,
            documents,
            top_k=5
        )

        print("\nRETRIEVED DOCUMENTS:\n")

        context_parts = []

        for i, doc in enumerate(
            documents,
            start=1
        ):

            matched_meta = None

            for original_doc, meta in zip(
                results["documents"],
                metadatas
            ):

                if original_doc == doc:

                    matched_meta = meta
                    break

            print(f"\nResult {i}")
            print("-" * 50)

            if matched_meta:
                if isinstance(matched_meta, dict):

                    print(
                        f"Source: "
                        f"{matched_meta.get('source', 'N/A')}"
                    )

            else:

                print(f"Source: {matched_meta}")


                print(
                    f"Type: "
                    f"{matched_meta.get('type', 'N/A')}"
                )

                print(
                    f"Page: "
                    f"{matched_meta.get('page', 'N/A')}"
                )

            print(doc[:500])

            if matched_meta:

                context_parts.append(
                    f"""
Source: {matched_meta.get('source', '')}
Type: {matched_meta.get('type', '')}
Page: {matched_meta.get('page', '')}

{doc}
"""
                )

            else:

                context_parts.append(doc)

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are an AI assistant for a Multimodal RAG system.
Use ONLY the provided context.

Pay attention to:
- Source
- Type
- Page
If the question is about a figure, image, diagram or chart:
1. Explain what the figure represents.
2. Explain the workflow or process shown.
3. Explain each important step or component.
4. Explain the purpose of the figure.
5. Do NOT use words such as:
- probably
- likely
- might
- appears to
Use only information present in the context.
If the question is about a table:
1. Explain the purpose of the table.
2. Explain important rows, columns and metrics.
3. Summarize key insights.
If the question asks:
- which report
- which source
- which document
use the Source metadata.
Do not invent information.

Context:
{context}

Question:
{query}

Answer:
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

    generator = AnswerGenerator()

    query = input("Enter query: ")

    answer = generator.generate_answer(
        query
    )

    print("\n")
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)