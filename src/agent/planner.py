import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from retrieval.query_router import QueryRouter


class Planner:

    def __init__(self):

        self.router = QueryRouter()

    def create_plan(self, query):

        query_type = self.router.route(query)

        if query_type == "text":

            return [
                "retrieve_text",
                "generate_answer"
            ]

        elif query_type == "table":

            return [
                "retrieve_table",
                "generate_answer"
            ]

        elif query_type == "image":

            return [
                "retrieve_image",
                "generate_answer"
            ]

        elif query_type == "report_summary":
            return [
            "report_summary_answer"
        ]

        elif query_type == "graphrag":
            return [
                "graphrag_answer"
            ]

        return [
            "generate_answer"
        ]


if __name__ == "__main__":

    planner = Planner()

    query = input("Enter query: ")

    plan = planner.create_plan(query)

    print(plan)