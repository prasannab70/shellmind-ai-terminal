from ai.ollama_client import ask_ollama
from ai.prompts import COMMAND_PROMPT


def ask_ai(query, context, os_type):

    # create prompt safely
    prompt = COMMAND_PROMPT
    prompt = prompt.replace("{query}", query)
    prompt = prompt.replace("{context}", context)
    prompt = prompt.replace("{os}", os_type)

    return ask_ollama(prompt)