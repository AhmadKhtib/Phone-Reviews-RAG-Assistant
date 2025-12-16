import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
import os
from functools import lru_cache
from typing import Dict, Any


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
# Add repo root (parent of /backend) to Python path so "Src" is importable


@lru_cache(maxsize=1)
def get_retriever():
    # IMPORTANT: this import must be fast and must NOT rebuild embeddings
    from Src.vectorizer import retriever
    return retriever


@lru_cache(maxsize=1)
def get_llm():
    # Fail fast if key missing
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def answer_question(query: str) -> Dict[str, Any]:
    r = get_retriever()
    llm = get_llm()

    docs = r.invoke(query)
    context = "\n\n".join([d.page_content for d in docs[:6]])

    system = SystemMessage(content="You are a helpful assistant for phone reviews. Use the provided context.")
    user = HumanMessage(content=f"Question: {query}\n\nContext:\n{context}")

    resp = llm.invoke([system, user])

    return {
        "answer": resp.content,
        "sources": [
            {"metadata": d.metadata, "snippet": d.page_content[:300]}
            for d in docs[:6]
        ],
    }
