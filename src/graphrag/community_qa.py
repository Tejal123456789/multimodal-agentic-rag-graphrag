from pathlib import Path
import ollama

COMMUNITY_SUMMARIES_DIR = Path(
    "data/graphrag/community_summaries"
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

def generate_community_answer(
    query,
    community_summary
):

    prompt = f"""
Answer the question using only the information provided in the community summary.

Community Summary:

{community_summary}

Question:

{query}

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

def merge_answers(
    query,
    partial_answers
):

    combined_answers = "\n\n".join(
        partial_answers
    )

    prompt = f"""
The following are answers from different communities of a document collection.

Combine them into one comprehensive answer.

Question:

{query}

Community Answers:

{combined_answers}

Final Comprehensive Answer:
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

def answer_query(
    query
):

    community_files = sorted(
        COMMUNITY_SUMMARIES_DIR.glob(
            "*.txt"
        )
    )

    partial_answers = []

    for community_file in community_files:

        community_summary = (
            read_community_summary(
                community_file
            )
        )

        answer = (
            generate_community_answer(
                query,
                community_summary
            )
        )

        partial_answers.append(
            answer
        )

    final_answer = merge_answers(
        query,
        partial_answers
    )

    return final_answer

if __name__ == "__main__":

    query = input(
        "Enter question: "
    )

    answer = answer_query(
        query
    )

    print(
        "\nFINAL GRAPHRAG ANSWER\n"
    )

    print(answer)