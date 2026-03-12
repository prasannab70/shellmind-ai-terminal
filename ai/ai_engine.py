from ai.ollama_client import ask_ollama
from ai.prompts import COMMAND_PROMPT


def ask_ai(query, context, os_type):

    # ensure safe values
    query = str(query).strip()
    context = str(context)
    os_type = str(os_type)

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

    if any(word in query_lower for word in explain_words):

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

        result = ask_ollama(prompt)

    # ------------------------------
    # COMMAND GENERATION MODE
    # ------------------------------

    else:

        prompt = COMMAND_PROMPT
        prompt = prompt.replace("{query}", query)
        prompt = prompt.replace("{context}", context)
        prompt = prompt.replace("{os}", os_type)

        result = ask_ollama(prompt)

    # ------------------------------
    # CLEAN LLM OUTPUT
    # ------------------------------

    if not result:
        return ""

    result = str(result).strip()

    # remove role artifacts
    if "role:" in result.lower():
        lines = result.splitlines()
        lines = [
            line for line in lines
            if not line.lower().startswith("role")
        ]
        result = "\n".join(lines).strip()

    return result