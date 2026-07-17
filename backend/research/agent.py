"""Research agent: a Gemini model equipped with the web_search skill.

The agent decides when to search, reads the results, and writes a grounded
answer. We also surface the raw sources it pulled so the API can return them.
"""
from google import genai
from google.genai import types
from django.conf import settings

from .tools import read_file, web_search

MODEL = "gemini-flash-lite-latest"

SYSTEM_INSTRUCTION = (
    "You are a research assistant. When a question needs current, factual, or "
    "niche information, use the web_search tool before answering. When the "
    "user refers to a document or file (.txt or .pdf) they've provided, use "
    "the read_file tool to read its contents before answering. Base your "
    "answer on the search results and file contents, be concise, and cite the "
    "sources you used by title. If the results do not answer the question, "
    "say so honestly."
)


def _extract_sources(afc_history) -> list[dict]:
    """Pull the search results out of the automatic-function-calling history."""
    sources: list[dict] = []
    for content in afc_history or []:
        for part in content.parts or []:
            fn_response = getattr(part, "function_response", None)
            if not fn_response:
                continue
            response = fn_response.response or {}
            # google-genai wraps a returned value under the "result" key; only
            # web_search returns a list of source dicts, so skip other tools
            # (e.g. read_file, which returns a plain string).
            result = response.get("result")
            if not isinstance(result, list):
                continue
            for item in result:
                if isinstance(item, dict) and item.get("link"):
                    sources.append(item)
    # De-duplicate by link while preserving order.
    seen, unique = set(), []
    for src in sources:
        if src["link"] not in seen:
            seen.add(src["link"])
            unique.append(src)
    return unique
    

def _build_prompt(query: str, memory) -> str:
    """Prepend the remembered conversation so the agent can recall earlier facts.

    ``memory`` is a list of the user's earlier messages, e.g.::

        ["My name is Hina.", "I like Python."]

    and the current query is ``"What language do I like?"``. Gemini then receives::

        Conversation:
        My name is Hina.
        I like Python.

        Question:
        What language do I like?
    """
    messages = [m.strip() for m in (memory or []) if m and m.strip()]
    if not messages:
        return query
    conversation = "\n".join(messages)
    return f"Conversation:\n{conversation}\n\nQuestion:\n{query}"


def run_research(query: str, memory=None) -> dict:
    """Run the research agent on a query.

    ``memory`` is an optional list of the user's earlier messages from the
    session; when provided, the agent can recall those earlier facts.

    Returns a dict with the final ``answer`` and the ``sources`` used.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=MODEL,
        contents=_build_prompt(query, memory),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[web_search, read_file],
        ),
    )

    return {
        "answer": (response.text or "").strip(),
        "sources": _extract_sources(response.automatic_function_calling_history),
    }
