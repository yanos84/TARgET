from typing import List
from ai_helper.indexer import SemanticUnit

"""
This module provides functionality for building prompts for the AI assistant based on
indexed semantic units and user queries. The build_prompt function takes a list of
SemanticUnit objects and a user query, and constructs a structured prompt that includes
a system message, the context derived from the semantic units, and the user's request.
The prompt is designed to guide the AI assistant in providing accurate and relevant
responses based on the existing codebase and its abstractions. The prompt emphasizes the
importance of adhering to existing APIs and class hierarchies, discouraging the AI from
inventing new APIs that are not present in the context. This structured approach helps
ensure that the AI assistant's responses are grounded in the actual code and documentation
of the toolkit.
"""


def build_prompt(units: List[SemanticUnit], user_query: str) -> str:
    """
    Constructs a prompt for the AI assistant based on the provided semantic units and
    user query. The prompt includes a system message, context derived from the semantic
    units, and the user's request. It emphasizes adherence to existing APIs and class
    hierarchies, discouraging the AI from inventing new APIs that are not present in
    the context.
    """
    blocks = []

    for u in units:
        # For methods, make the owning class explicit so the model doesn't
        # confuse a method with a free-standing function of the same name.
        name_line = f"{u.parent}.{u.name}" if u.parent else u.name

        block = (
            f"[TYPE] {u.kind}\n"
            f"[NAME] {name_line}\n"
            f"[FILE] {u.file}\n"
            f"[SIGNATURE] {u.signature}\n"
            f"[DOCSTRING]\n{u.docstring}\n"
        )
        blocks.append(block)

    context = "\n".join(blocks)

    prompt = (
        "SYSTEM:\n"
        "You are an AI assistant specialized in this Python toolkit.\n"
        "You must strictly follow existing abstractions and class hierarchies.\n"
        "Do NOT invent APIs.\n\n"
        "CONTEXT:\n"
        f"{context}\n\n"
        "USER REQUEST:\n"
        f"{user_query}\n"
    )

    return prompt