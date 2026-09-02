import chromadb
import re
from sentence_transformers import SentenceTransformer


class HybridRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="vector_store/chroma_db"
        )

        self.collection = self.client.get_collection(
            "multimodal_rag"
        )

    def retrieve(
        self,
        query,
        top_k=5
    ):

        report_filter = None
        match = re.search(

            r"report\d+",
            query.lower()
        )

        if match:
            report_filter = match.group()
            print(
                f"Detected report filter: {report_filter}"
        )

        query_embedding = self.model.encode(
            query
        ).tolist()

        if report_filter:

            print("Applying filter:", report_filter)

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

        else:

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            print("\nMetadata Example:")
            print(results["metadatas"][0][0])

        print("\nRETRIEVED RESULTS\n")

        for metadata, document in zip(
            results["metadatas"],
            results["documents"]
        ):

            print("=" * 50)

            print(metadata)

            print(document[:300])

        return {
                    "documents": results["documents"][0],
                    "metadatas": results["metadatas"][0]
                }


if __name__ == "__main__":

    retriever = HybridRetriever()

    query = input("Enter query: ")

    results = retriever.retrieve(
        query
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    print("\nTop Results:\n")

    for i, (doc,  meta) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        print(f"\nResult {i}")
    
        print(
            f"Source: {meta.get('source', 'N/A')}"
        )

        print(
            f"Type: {meta.get('type', 'N/A')}"
        )

        print(
            f"Page: {meta.get('page', 'N/A')}"
        )

        print("-" * 50)

        print(doc[:1000])