from ai.ollama_client import ask_ollama
from ai.prompts import COMMAND_PROMPT


def ask_ai(query, context, os_type):

    query_lower = query.lower()

    # detect explanation queries
    explain_words = [
        "what is",
        "meaning",
        "explain",
        "define",
        "tell me about",
        "what does",
        "how does"
    ]

    # ------------------------------
    # EXPLANATION MODE
    # ------------------------------

    if any(w in query_lower for w in explain_words):

        prompt = f"""
You are an AI developer assistant.

Explain the following command or concept clearly and shortly.

User Query:
{query}

Operating System:
{os_type}

Project Context:
{context}
"""

        return ask_ollama(prompt)

    # ------------------------------
    # COMMAND GENERATION MODE
    # ------------------------------

    prompt = COMMAND_PROMPT
    prompt = prompt.replace("{query}", query)
    prompt = prompt.replace("{context}", context)
    prompt = prompt.replace("{os}", os_type)

    result = ask_ollama(prompt)

    # clean accidental role outputs from LLM
    if "role:" in result.lower():
        lines = result.splitlines()
        lines = [l for l in lines if not l.lower().startswith("role")]
        result = "\n".join(lines).strip()

    return result