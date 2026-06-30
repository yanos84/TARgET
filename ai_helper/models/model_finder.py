from pathlib import Path

"""
This module provides functions for listing and selecting local LLM models stored in a specified directory. It includes functionality to list all available models with their sizes and allows the user to choose a model by entering its corresponding number. The selected model's path can then be used for further processing, such as loading the model for inference or training.   
"""

def list_models(models_dir: str):
    """
    List all ``.gguf`` models in the specified directory.

    :param models_dir: Path to the directory containing ``.gguf`` model files.
    :type models_dir: str

    :returns: A sorted list of ``Path`` objects representing the ``.gguf`` model files.
    :rtype: List[pathlib.Path]

    :raises FileNotFoundError: If the specified models directory does not exist.
    :raises RuntimeError: If no ``.gguf`` models are found in the specified directory.
    """
    models_path = Path(models_dir)
    if not models_path.exists():
        raise FileNotFoundError(f"Models directory not found: {models_dir}")

    models = sorted(models_path.glob("*.gguf"))
    if not models:
        raise RuntimeError("No .gguf models found in models directory")

    return models

def choose_model(models):
    """
    Prompt the user to select a model from the provided list of models.

    :param models: A list of Path objects representing the available models.
    :type models: List[Path]

    :returns: The selected model's path.
    :rtype: Path
    """
    print("\nAvailable models:\n")
    for i, model in enumerate(models):
        size_gb = model.stat().st_size / (1024**3)
        print(f"[{i}] {model.name}  ({size_gb:.2f} GB)")

    while True:
        choice = input("\nSelect model number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(models):
                return models[idx]

        print("Invalid selection!! try again.")
