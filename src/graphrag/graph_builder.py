import json
from pathlib import Path

SUMMARIES_DIR = Path(
    "data/graphrag/document_summaries"
)

TOPICS_DIR = Path(
    "data/graphrag/topics"
)

import ollama


def extract_topics(
    summary_text
):

    prompt = f"""
Extract 5 to 10 main topics from the following research paper summary.

Return only a simple list of topics.

Summary:

{summary_text}
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

def read_summary(
    summary_file
):

    with open(
        summary_file,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def save_topics(
    output_file,
    topics
):

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(topics)

def read_topics(
    topic_file
):

    with open(
        topic_file,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def get_report_name(
    topic_file
):

    return (
        topic_file.stem
        .replace("_chunks_topics", "")
    )

def create_empty_graph():

    graph = {}

    topic_files = list(
        TOPICS_DIR.glob("*.txt")
    )

    for topic_file in topic_files:

        report_name = get_report_name(
            topic_file
        )

        graph[report_name] = []

    return graph

def topic_overlap(
    topics1,
    topics2
):

    topics1 = set(
        line.strip().lower()
        for line in topics1.splitlines()
        if line.strip()
    )

    topics2 = set(
        line.strip().lower()
        for line in topics2.splitlines()
        if line.strip()
    )

    return len(
        topics1.intersection(
            topics2
        )
    )

def build_graph_connections():

    graph = create_empty_graph()

    topic_files = list(
        TOPICS_DIR.glob("*.txt")
    )

    for i in range(
        len(topic_files)
    ):

        for j in range(
            i + 1,
            len(topic_files)
        ):

            report1 = get_report_name(
                topic_files[i]
            )

            report2 = get_report_name(
                topic_files[j]
            )

            topics1 = read_topics(
                topic_files[i]
            )

            topics2 = read_topics(
                topic_files[j]
            )

            overlap = topic_overlap(
                topics1,
                topics2
            )

            if overlap > 0:

                graph[report1].append(
                    report2
                )

                graph[report2].append(
                    report1
                )

    return graph

graph = build_graph_connections()

print("\nGRAPH CONNECTIONS:\n")

for report, connections in graph.items():

    print(
        f"{report} -> {len(connections)} connections"
    )


if __name__ == "__main__":

    summary_files = list(
        SUMMARIES_DIR.glob("*.txt")
    )

    print(
        f"Found {len(summary_files)} summaries."
    )

    for summary_file in summary_files:

        output_file = (
            TOPICS_DIR
            /
            summary_file.name.replace(
                "_summary.txt",
                "_topics.txt"
            )
        )

        if output_file.exists():

            print(
                f"Skipping {output_file.name}"
            )

            continue

        print(
            f"\nProcessing {summary_file.name}"
        )

        summary_text = read_summary(
            summary_file
        )

        topics = extract_topics(
            summary_text
        )

        save_topics(
            output_file,
            topics
        )

        print(
            f"Saved {output_file.name}"
        )

    topic_files = list(
        TOPICS_DIR.glob("*.txt")
    )

    print(
        f"\nFound {len(topic_files)} topic files."
    )

    graph = create_empty_graph()

    print("\nGRAPH NODES:\n")

    for node in graph:

        print(node)