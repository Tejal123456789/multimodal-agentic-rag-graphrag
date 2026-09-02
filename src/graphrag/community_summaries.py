from pathlib import Path
import json
import ollama

GRAPH_FILE = Path(
    "data/graphrag/graph/report_graph.json"
)

SUMMARIES_DIR = Path(
    "data/graphrag/document_summaries"
)

COMMUNITY_SUMMARIES_DIR = Path(
    "data/graphrag/community_summaries"
)

def load_graph():

    with open(
        GRAPH_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def find_communities(
    graph
):

    visited = set()

    communities = []

    for report in graph:

        if report in visited:
            continue

        community = []

        stack = [report]

        while stack:

            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            community.append(node)

            neighbors = [
                edge["report"]
                for edge in graph[node]
            ]

            stack.extend(
                neighbors
            )

        communities.append(
            community
        )

    return communities

def read_report_summary(
    report_name
):

    summary_file = (
        SUMMARIES_DIR
        /
        f"{report_name}_chunks_summary.txt"
    )

    with open(
        summary_file,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def collect_community_content(
    community
):

    combined_text = ""

    for report in community:

        summary = read_report_summary(
            report
        )

        combined_text += (
            f"\n\n=== {report} ===\n\n"
        )

        combined_text += summary

    return combined_text

def generate_community_summary(
    community_text
):

    prompt = f"""
Create a single summary for this community of related research papers.

Include:

1. Main research area
2. Common themes
3. Key methods
4. Important findings

Community Content:

{community_text}
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

def save_community_summary(
    community_id,
    summary
):

    output_file = (
        COMMUNITY_SUMMARIES_DIR
        /
        f"community_{community_id}.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(summary)

if __name__ == "__main__":

    graph = load_graph()

    communities = find_communities(
        graph
    )

    print(
        f"Found {len(communities)} communities."
    )

    for idx, community in enumerate(
        communities,
        start=1
    ):

        print(
            f"\nProcessing Community {idx}"
        )

        community_text = (
            collect_community_content(
                community
            )
        )

        summary = (
            generate_community_summary(
                community_text
            )
        )

        save_community_summary(
            idx,
            summary
        )

        print(
            f"Saved community_{idx}.txt"
        )
