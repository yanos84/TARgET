from typing import List
from ai_helper.indexer import SemanticUnit


def build_prompt(units: List[SemanticUnit], user_query: str) -> str:
    blocks = []

    for u in units:
        block = (
            f"[TYPE] {u.kind}\n"
            f"[NAME] {u.name}\n"
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
