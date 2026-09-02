import json
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)
from graphrag.community_detector import (
    find_communities
)
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

def build_networkx_graph(
    graph_data
):

    G = nx.Graph()

    for report, connections in graph_data.items():

        G.add_node(report)

        for connection in connections:

            target_report = (
                connection["report"]
            )

            similarity = (
                connection["similarity"]
            )

            G.add_edge(
                report,
                target_report,
                weight=similarity
            )

    return G

def visualize_graph(
    G,
    communities
):

    plt.figure(
        figsize=(12, 8)
    )

    pos = nx.spring_layout(
        G,
        seed=42
    )

    node_colors = assign_community_colors(
        G,
        communities
    )

    edge_labels = nx.get_edge_attributes(
         G,
        "weight"
    )

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1500,
        node_color=node_colors,
        font_size=8,
        font_weight="bold"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={
            edge: round(weight, 2)
            for edge, weight
            in edge_labels.items()
    },
    font_size=8
)

    plt.title(
        "GraphRAG Report Knowledge Graph"
    )

    plt.savefig(
        "report_graph_visualization.png"
    )

    plt.show()

def assign_community_colors(
    G,
    communities
):

    color_map = {}

    colors = [
        "red",
        "green",
        "orange",
        "purple",
        "yellow",
        "pink",
        "cyan",
        "brown",
        "lime",
        "gold",
        "gray"
    ]

    for idx, community in enumerate(
        communities
    ):

        color = colors[
            idx % len(colors)
        ]

        for node in community:

            color_map[node] = color

    node_colors = []

    for node in G.nodes():

        node_colors.append(
            color_map.get(
                node,
                "lightgray"
            )
        )

    return node_colors

if __name__ == "__main__":

    graph_data = load_graph()

    G = build_networkx_graph(
        graph_data
    )

    communities = find_communities(
        graph_data
    )

    print(
        f"Nodes: {G.number_of_nodes()}"
    )

    print(
        f"Edges: {G.number_of_edges()}"
    )

    visualize_graph(
        G,
        communities
)

    