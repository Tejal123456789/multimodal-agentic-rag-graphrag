import json
from pathlib import Path


class TableProcessor:

    def __init__(
        self,
        table_dir="data/extracted/tables",
        output_dir="data/processing/table_summaries"
    ):
        self.table_dir = Path(table_dir)
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def summarize_table(self, table):

        rows = table.get("rows", 0)
        columns = table.get("columns", 0)

        data = table.get("data", [])

        summary = (
            f"Table found on page "
            f"{table['page_number']}. "
            f"It contains {rows} rows and "
            f"{columns} columns. "
        )

        if data:

            header = data[0]

            header_text = ", ".join(
                str(cell)
                for cell in header
                if cell
            )

            summary += (
                f"Column headers are: "
                f"{header_text}. "
            )

            for row in data[1:4]:

                row_text = ", ".join(
                    str(cell)
                    for cell in row
                    if cell
                )

                if row_text:

                    summary += (
                        f"Example row: "
                        f"{row_text}. "
                    )

        return summary

    def process_document(self, json_file):

        with open(json_file, "r", encoding="utf-8") as f:
            tables = json.load(f)

        summaries = []

        for table in tables:

            summaries.append(
                {
                    "table_id": table["table_id"],
                    "page": table["page_number"],
                    "summary": self.summarize_table(table)
                }
            )

        output_file = (
            self.output_dir /
            f"{json_file.stem}_summaries.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(summaries, f, indent=4)

        print(
            f"{json_file.stem}: "
            f"{len(summaries)} summaries created"
        )

    def process_all_documents(self):

        for json_file in self.table_dir.glob("*.json"):

            self.process_document(json_file)


if __name__ == "__main__":

    processor = TableProcessor()

    processor.process_all_documents()