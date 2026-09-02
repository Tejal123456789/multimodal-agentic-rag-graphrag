import sys
from pathlib import Path
from graphrag.community_qa import answer_query
from graphrag.report_summary_qa import (
    answer_report_query
)
sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from retrieval.hybrid_retriever import HybridRetriever
from llm.answer_generator import AnswerGenerator


class AgentTools:

    def __init__(self):

        self.retriever = HybridRetriever()
        self.answer_generator = AnswerGenerator()

    def retrieve_text(self, query):

        return self.retriever.retrieve(
            query,
            top_k=10
        )

    def retrieve_table(self, query):

        return self.retriever.retrieve(
            query,
            top_k=10
        )

    def retrieve_image(self, query):

        return self.retriever.retrieve(
            query,
            top_k=10
        )

    def generate_answer(self, query):

        return self.answer_generator.generate_answer(
            query
        )

    def report_summary_answer(
        self,
        query
    ):

        return answer_report_query(
        query
    )
    def graphrag_answer(
        self,
        query
        ):

        return answer_query(
        query
        )


if __name__ == "__main__":

    tools = AgentTools()

    answer = tools.generate_answer(
        "What is conformal prediction?"
    )

    print(answer)