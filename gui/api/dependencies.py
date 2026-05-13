from ai_helper.indexer import index_toolkit
from ai_helper.retriever import SemanticRetriever
from llama_cpp import Llama
from pathlib import Path

MODELS_DIR = Path("ai_helper/models")
TOOLKIT_DIR = Path("/run/media/yanos/48D8EB77D8EB6224/Python_projects/TARgET/")

# --- load toolkit once ---
units = index_toolkit(str(TOOLKIT_DIR))
retriever = SemanticRetriever(units)

# --- model registry ---
_loaded_models = {}

def get_model(model_name: str):
    if model_name not in _loaded_models:
        model_path = MODELS_DIR / model_name
        _loaded_models[model_name] = Llama(
            model_path=str(model_path),
            n_ctx=2048,
            n_threads=8,
            verbose=False
        )
    return _loaded_models[model_name]
