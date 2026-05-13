from pathlib import Path

def list_models(models_dir: str):
    models_path = Path(models_dir)
    if not models_path.exists():
        raise FileNotFoundError(f"Models directory not found: {models_dir}")

    models = sorted(models_path.glob("*.gguf"))
    if not models:
        raise RuntimeError("No .gguf models found in models directory")

    return models

def choose_model(models):
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
