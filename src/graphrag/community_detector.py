import json
from pathlib import Path

GRAPH_FILE = Path(
    "data/graphrag/graph/report_graph.json"
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

if __name__ == "__main__":

    graph = load_graph()

    communities = find_communities(
        graph
    )

    print(
        f"Found {len(communities)} communities.\n"
    )

    for idx, community in enumerate(
        communities,
        start=1
    ):

        print(
            f"Community {idx}:"
        )

        print(community)

        print()