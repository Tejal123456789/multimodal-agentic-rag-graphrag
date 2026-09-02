from pathlib import Path
import ollama

SUMMARIES_DIR = Path(
    "data/graphrag/document_summaries"
)

import re


def load_report_summary(
    report_number
):

    summary_file = (
        SUMMARIES_DIR /
        f"report{report_number}_chunks_summary.txt"
    )

    with open(
        summary_file,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def answer_report_query(
    query
):

    match = re.search(
        r"report\s*(\d+)",
        query.lower()
    )

    if not match:

        return (
            "Please specify a report number."
        )

    report_number = match.group(1)

    summary = load_report_summary(
        report_number
    )

    prompt = f"""
You are answering questions about a
single report.

Report Summary:

{summary}

User Question:

{query}

If the user asks for a summary table,
create a report overview table.

Include:

1. Research Area
2. Problem Addressed
3. Main Topics
4. Key Methods
5. Datasets Used
6. Key Findings
7. Applications
8. Limitations (if available)

The goal is to help a person who has never read
the report understand it quickly.

Do not reproduce tables from the report.
Create a high-level report summary table.

Answer:
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