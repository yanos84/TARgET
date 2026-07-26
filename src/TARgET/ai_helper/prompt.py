from typing import List

from ai_helper.indexer import SemanticUnit


def build_prompt(
    units: List[SemanticUnit],
    user_query: str,
) -> str:
    """
    Builds an LLM prompt containing the actual source code of the most relevant
    retrieved units.
    """

    blocks = []

    for unit in units:

        name = (
            f"{unit.parent}.{unit.name}"
            if unit.parent
            else unit.name
        )

        metadata = (
            f"[TYPE] {unit.kind}\n"
            f"[NAME] {name}\n"
            f"[FILE] {unit.file}\n"
            f"[MODULE] {unit.module}\n"
            f"[SIGNATURE] {unit.signature}\n"
        )

        if unit.bases:
            metadata += (
                f"[BASES] "
                f"{', '.join(unit.bases)}\n"
            )

        if unit.decorators:
            metadata += (
                f"[DECORATORS] "
                f"{', '.join(unit.decorators)}\n"
            )

        block = (
            f"{metadata}\n"
            f"[DOCSTRING]\n"
            f"{unit.docstring}\n\n"
            f"[SOURCE CODE]\n"
            f"{unit.code}\n"
        )

        blocks.append(block)

    context = "\n".join(blocks)

    return (
        "SYSTEM:\n"
        "You are an AI assistant specialized in this Python toolkit.\n\n"

        "The CONTEXT contains actual source code extracted from the toolkit.\n"
        "Use the source code as the primary source of truth.\n\n"

        "You must:\n"
        "- follow the existing implementation;\n"
        "- respect existing class hierarchies and abstractions;\n"
        "- use existing names and interfaces;\n"
        "- explain behavior based on the provided source code;\n"
        "- avoid inventing APIs or implementations that are not supported by "
        "the source code.\n\n"

        "If the provided context is insufficient to answer the question, "
        "say so explicitly instead of guessing.\n\n"

        "CONTEXT:\n"
        f"{context}\n\n"

        "USER REQUEST:\n"
        f"{user_query}\n"
    )