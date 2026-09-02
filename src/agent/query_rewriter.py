import ollama


class QueryRewriter:

    def __init__(self):

        self.followup_words = [
            "it",
            "this",
            "that",
            "them",
            "these",
            "those",
            "previous",
            "above",
            "earlier"
        ]

    def needs_rewrite(
        self,
        query
    ):

        query = query.lower()

        for word in self.followup_words:

            if word in query.split():
                return True

        return False

    def rewrite_query(
        self,
        query,
        chat_history
    ):

        prompt = f"""
You are a query rewriter.

Convert the current question into a
standalone question using the conversation history.

If the question is already standalone,
return it unchanged.

Conversation History:
{chat_history}

Current Question:
{query}

Standalone Question:
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

        return response["message"]["content"].strip()

# if __name__ == "__main__":

#     history = """
# User: What is conformal prediction?
# Assistant: Conformal prediction returns a set of labels ...
# """

#     query = "Can you explain it simply?"

#     rewriter = QueryRewriter()

#     print(
#         rewriter.rewrite_query(
#             query,
#             history
#         )
#     )