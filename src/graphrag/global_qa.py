from pathlib import Path
import ollama

GLOBAL_SUMMARY_FILE = Path(
    "data/graphrag/global_summary/global_summary.txt"
)

def load_global_summary():

    with open(
        GLOBAL_SUMMARY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

def answer_global_question(
    query,
    global_summary
):

    prompt = f"""
You are answering questions about an entire collection of research papers.

Use only the information provided in the global summary.

Global Summary:

{global_summary}

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

if __name__ == "__main__":

    global_summary = load_global_summary()

    query = input(
        "Enter global question: "
    )

    answer = answer_global_question(
        query,
        global_summary
    )

    print("\nANSWER:\n")

    print(answer)