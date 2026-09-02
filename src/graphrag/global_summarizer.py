from pathlib import Path
import ollama

COMMUNITY_SUMMARIES_DIR = Path(
    "data/graphrag/community_summaries"
)

GLOBAL_SUMMARY_DIR = Path(
    "data/graphrag/global_summary"
)

GLOBAL_SUMMARY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def read_community_summary(
    file_path
):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def collect_global_content():

    combined_text = ""

    summary_files = sorted(
        COMMUNITY_SUMMARIES_DIR.glob("*.txt")
    )

    for summary_file in summary_files:

        summary = read_community_summary(
            summary_file
        )

        combined_text += (
            f"\n\n=== {summary_file.stem} ===\n\n"
        )

        combined_text += summary

    return combined_text

def generate_global_summary(
    global_content
):

    prompt = f"""
Generate a comprehensive summary of the complete document collection.

Include:

1. Major research domains
2. Common themes across communities
3. Important methods and technologies
4. Key findings and insights
5. Overall trends observed in the corpus

Community Summaries:

{global_content}
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

def save_global_summary(
    summary
):

    output_file = (
        GLOBAL_SUMMARY_DIR
        / "global_summary.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(summary)

if __name__ == "__main__":

    global_content = (
        collect_global_content()
    )

    summary = (
        generate_global_summary(
            global_content
        )
    )

    save_global_summary(
        summary
    )

    print(
        "Global summary saved."
    )