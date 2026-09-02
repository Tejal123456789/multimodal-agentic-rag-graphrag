import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from agent.agent_executor import AgentExecutor
from agent.query_rewriter import QueryRewriter

st.set_page_config(
    page_title="Multimodal Agentic RAG",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Multimodal Agentic RAG System")

st.markdown(
    """
Ask questions about text, tables, and figures from the research paper collection.
"""
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.chat_input(
    "Ask your question..."
)

if query:

    rewritten_query = query

    rewriter = QueryRewriter()

    if (
        rewriter.needs_rewrite(query)
        and len(st.session_state.chat_history) > 0
    ):

        chat_history_text = ""

        for chat in st.session_state.chat_history:

            chat_history_text += (
                f"User: {chat['question']}\n"
            )

            chat_history_text += (
                f"Assistant: {chat['answer']}\n\n"
            )

        rewritten_query = (
            rewriter.rewrite_query(
                query,
                chat_history_text
            )
        )

    with st.spinner(
        "Generating answer..."
    ):

        agent = AgentExecutor()

        answer = agent.run(
        rewritten_query
    )

    st.session_state.chat_history.append(
        {
            "question": query,
            "answer": answer
        }
    )

for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])