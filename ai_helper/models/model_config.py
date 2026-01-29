# model_config.py
from pathlib import Path

CONFIG_FILE = Path.home() / ".target_ai_model"

def save_model(path: str):
    CONFIG_FILE.write_text(path)

def load_model():
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()
    return None
