from llama_cpp import Llama
from ai_helper.indexer import index_toolkit
from ai_helper.retriever import SemanticRetriever
from ai_helper.prompt import build_prompt
from ai_helper.models.model_finder import list_models, choose_model
from ai_helper.models.model_config import load_model, save_model
from pathlib import Path

'''
This module serves as the main entry point for the AI assistant. It handles loading the LLM model, 
indexing the codebase, and processing user queries. The module first checks for a saved model path
 and loads it if available; otherwise, it lists available models and prompts the user to select one. 
 After loading the model, it indexes the toolkit using the index_toolkit function and initializes a 
 SemanticRetriever with the indexed units. The ask function takes a user query, retrieves relevant semantic units, 
 builds a prompt using the build_prompt function, and generates a response from the LLM. Finally, 
 it prints the response to the user. This structured approach allows for efficient interaction with 
 the AI assistant while leveraging the existing codebase effectively. 
'''


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
 
