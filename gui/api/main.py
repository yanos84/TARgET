from fastapi import FastAPI, HTTPException
from gui.api.models import AskRequest, AskResponse
from gui.api.dependencies import retriever, get_model, MODELS_DIR
from ai_helper.prompt import build_prompt

app = FastAPI(title="TARgET AI Helper")

@app.get("/models")
def list_models():
    return [p.name for p in MODELS_DIR.glob("*.gguf")]

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, model: str):
    model_path = MODELS_DIR / model
    if not model_path.exists():
        raise HTTPException(404, "Model not found")

    llm = get_model(model)

    relevant = retriever.retrieve(req.question, top_k=req.top_k)
    prompt = build_prompt(relevant, req.question)

    output = llm(prompt, max_tokens=512, stop=["<|EOT|>"])

    return AskResponse(
        answer=output["choices"][0]["text"].strip(),
        model=model
    )
