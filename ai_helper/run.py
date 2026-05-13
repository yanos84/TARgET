from llama_cpp import Llama
from ai_helper.indexer import index_toolkit
from ai_helper.retriever import SemanticRetriever
from ai_helper.prompt import build_prompt
from ai_helper.models.model_finder import list_models, choose_model
from ai_helper.models.model_config import load_model, save_model
from pathlib import Path


MODELS_DIR = "/run/media/yanos/48D8EB77D8EB6224/Python_projects/TARgET/ai_helper/models"

saved = load_model()
if saved and Path(saved).exists():
    model_path = Path(saved)
else:
    models = list_models(MODELS_DIR)
    model_path = choose_model(models)
    save_model(str(model_path))

print(f"\n Loading model: {model_path.name}\n")

llm = Llama(
    model_path=str(model_path),
    n_ctx=2048,
    n_threads=8,
    verbose=False
)


# Index toolkit
units = index_toolkit("/run/media/yanos/48D8EB77D8EB6224/Python_projects/TARgET")
retriever = SemanticRetriever(units)
def ask(query: str):
    retrieved = retriever.retrieve(query)
    prompt = build_prompt(retrieved, query)

    output = llm(
        prompt,
        max_tokens=512,
        temperature=0.2,
        stop=["</s>"]
    )

    print(output["choices"][0]["text"])

if __name__== "__main__":
   ask("Explain how RankedBottomUpAcceptor works")
 
