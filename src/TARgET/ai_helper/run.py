import argparse
import os
from pathlib import Path

from llama_cpp import Llama
from ai_helper.indexer import index_toolkit
from ai_helper.retriever import SemanticRetriever
from ai_helper.prompt import build_prompt
from ai_helper.models.model_finder import list_models, choose_model
from ai_helper.models.model_config import load_model, save_model

"""
This module serves as the main entry point for the AI assistant. It handles loading the LLM model,
indexing the codebase, and processing user queries. The module first checks for a saved model path
and loads it if available; otherwise, it lists available models and prompts the user to select one.
After loading the model, it indexes the toolkit using the index_toolkit function and initializes a
SemanticRetriever with the indexed units. The ask function takes a user query, retrieves relevant
semantic units, builds a prompt using the build_prompt function, and generates a response from the
LLM. Finally, it prints the response to the user.

Paths are no longer hardcoded: MODELS_DIR and the toolkit path are read from environment variables
(TARGET_MODELS_DIR, TARGET_TOOLKIT_PATH) or CLI flags, falling back to sensible defaults relative
to this file, so any contributor can run this on their own machine without editing source.
"""

# Default toolkit path: parent of the ai_helper package (i.e. the project root).
DEFAULT_TOOLKIT_PATH = Path(__file__).resolve().parent.parent
# Default models dir: a "models" folder alongside this file, unless overridden.
DEFAULT_MODELS_DIR = Path(__file__).resolve().parent / "models" / "gguf"


def get_model_path(models_dir: str) -> Path:
    """
    Loads a previously saved model path if it still exists on disk; otherwise lists
    available .gguf models in models_dir and prompts the user to choose one, saving
    the choice for next time.
    """
    saved = load_model()
    if saved and Path(saved).exists():
        return Path(saved)

    models = list_models(models_dir)
    model_path = choose_model(models)
    save_model(str(model_path))
    return model_path


def build_assistant(toolkit_path: str, models_dir: str):
    """
    Loads the LLM and indexes the given toolkit path, returning (llm, retriever)
    ready to be used by ask().
    """
    model_path = get_model_path(models_dir)
    print(f"\n Loading model: {model_path.name}\n")

    llm = Llama(
        model_path=str(model_path),
        n_ctx=2048,
        n_threads=8,
        verbose=False,
    )

    print(f"Indexing toolkit: {toolkit_path}")
    units = index_toolkit(toolkit_path)
    print(f"Indexed {len(units)} semantic units\n")
    retriever = SemanticRetriever(units)

    return llm, retriever


def ask(llm, retriever, query: str):
    retrieved = retriever.retrieve(query)
    prompt = build_prompt(retrieved, query)

    output = llm(
        prompt,
        max_tokens=512,
        temperature=0.2,
        stop=["</s>"],
    )

    print(output["choices"][0]["text"])


def main():
    parser = argparse.ArgumentParser(description="Ask the toolkit assistant a question.")
    parser.add_argument(
        "query",
        nargs="?",
        default="Explain how RankedBottomUpAcceptor works",
        help="Question to ask about the toolkit.",
    )
    parser.add_argument(
        "--toolkit-path",
        default=os.environ.get("TARGET_TOOLKIT_PATH", str(DEFAULT_TOOLKIT_PATH)),
        help="Path to the codebase to index. Defaults to $TARGET_TOOLKIT_PATH or the project root.",
    )
    parser.add_argument(
        "--models-dir",
        default=os.environ.get("TARGET_MODELS_DIR", str(DEFAULT_MODELS_DIR)),
        help="Directory containing .gguf model files. Defaults to $TARGET_MODELS_DIR.",
    )
    args = parser.parse_args()

    llm, retriever = build_assistant(args.toolkit_path, args.models_dir)
    ask(llm, retriever, args.query)


if __name__ == "__main__":
    main()