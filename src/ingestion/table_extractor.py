import pdfplumber


class TableExtractor:

    def extract_tables(self, pdf_path):

        extracted_tables = []

        with pdfplumber.open(pdf_path) as pdf:

            for page_num, page in enumerate(pdf.pages):

                tables = page.extract_tables(
                    table_settings={
                        "vertical_strategy": "lines",
                        "horizontal_strategy": "lines",
                        "snap_tolerance": 3,
                        "join_tolerance": 3,
                        "edge_min_length": 3,
                        "min_words_vertical": 2,
                        "min_words_horizontal": 1
                    }
                )

                print(
                    f"Page {page_num + 1}: "
                    f"{len(tables)} tables found"
                )

                for table_index, table in enumerate(tables):

                    # Skip empty tables
                    if not table:
                        continue

                    # Count non-empty cells
                    cell_count = sum(
                        1
                        for row in table
                        if row
                        for cell in row
                        if cell not in (None, "")
                    )

                    # Ignore very tiny detections
                    if cell_count < 4:
                        continue

                    max_columns = max(
                        len(row)
                        for row in table
                        if row
                    )

                    # Ignore text blocks disguised as tables
                    if max_columns < 2:
                        continue

                    extracted_tables.append(
                        {
                            "page_number": page_num + 1,
                            "table_id": (
                                f"table_{page_num + 1}_{table_index + 1}"
                            ),
                            "rows": len(table),
                            "columns": max_columns,
                            "data": table
                        }
                    )

        return extracted_tables