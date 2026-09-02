import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from agent.planner import Planner
from agent.tools import AgentTools


class AgentExecutor:

    def __init__(self):

        self.planner = Planner()
        self.tools = AgentTools()

    def run(self, query):

        plan = self.planner.create_plan(query)

        print("\nPlan:")
        print(plan)

        result = None

        for step in plan:

            if step == "retrieve_text":

                result = self.tools.retrieve_text(query)

            elif step == "retrieve_table":

                result = self.tools.retrieve_table(query)
                print(result)

            elif step == "retrieve_image":

                result = self.tools.retrieve_image(query)

            elif step == "generate_answer":

                result = self.tools.generate_answer(query)

            elif step == "report_summary_answer":

                result = (
                    self.tools
                    .report_summary_answer(
                    query
                )
            )
            elif step == "graphrag_answer":
                result = self.tools.graphrag_answer(
                    query
                )

        return result


if __name__ == "__main__":

    agent = AgentExecutor()

    query = input("Enter query: ")

    answer = agent.run(query)

    print("\n")
    print("=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)
    print(answer)