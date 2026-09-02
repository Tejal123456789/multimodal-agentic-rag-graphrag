class QueryRouter:

    def route(self, query):

        query = query.lower()

        if any(
            word in query
            for word in [
                "major themes",
                "all reports",
                "all documents",
                "dataset",
                "research domains",
                "complete collection",
                "entire collection",
                "across all reports",
                "across the corpus",
                "common trends",
                "summarize all reports",
                "summarize the dataset"
            ]
        ):
            return "graphrag"

        elif (
            "report" in query
            and any(
                word in query
                for word in [
                "summary",
                "summarize",
                "table",
                "key findings",
                "overview"
            ]
        )
    ):
            return "report_summary"

        elif any(
            word in query
            for word in [
            "figure",
            "image",
            "diagram",
            "chart",
            "graph"
        ]
    ):
            return "image"

        elif any(
            word in query
            for word in [
            "table",
            "tabular"
        ]
    ):
            return "table"

        else:
            return "text"

if __name__ == "__main__":

    router = QueryRouter()

    query = input("Enter query: ")

    print(
        router.route(query)
    )