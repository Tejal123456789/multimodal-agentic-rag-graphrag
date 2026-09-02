from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
GRAPH_FILE = Path(
    "data/graphrag/graph/report_graph.json"
)

TOPICS_DIR = Path(
    "data/graphrag/topics"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def read_topics(
    topic_file
):

    with open(
        topic_file,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def calculate_similarity(
    topics1,
    topics2
):

    embedding1 = model.encode(
        topics1
    )

    embedding2 = model.encode(
        topics2
    )

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return similarity

import json


def save_graph(
    graph,
    output_file
):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            graph,
            f,
            indent=4
        )

if __name__ == "__main__":

    topic_files = list(
        TOPICS_DIR.glob("*.txt")
    )

    graph = {}

    for topic_file in topic_files:

        report_name = (
            topic_file.stem
            .replace("_chunks_topics", "")
        )

        graph[report_name] = []

    for i in range(
        len(topic_files)
    ):

        for j in range(
            i + 1,
            len(topic_files)
        ):

            topics1 = read_topics(
                topic_files[i]
            )

            topics2 = read_topics(
                topic_files[j]
            )

            similarity = calculate_similarity(
                topics1,
                topics2
            )

            if similarity >= 0.50:

                report1 = (
                    topic_files[i].stem
                    .replace(
                        "_chunks_topics",
                        ""
                    )
                )

                report2 = (
                    topic_files[j].stem
                    .replace(
                        "_chunks_topics",
                        ""
                    )
                )

                graph[report1].append(
                    {
                        "report": report2,
                        "similarity": float(
                            round(
                                similarity,
                                4
                            )
                        )
                    }
                )

                graph[report2].append(
                    {
                        "report": report1,
                        "similarity": float(
                            round(
                                similarity,
                                4
                            )
                        )
                    }
                )

    save_graph(
        graph,
        GRAPH_FILE
    )

    print(
        f"Graph saved to {GRAPH_FILE}"
    )
