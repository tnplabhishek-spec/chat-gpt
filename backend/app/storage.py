import json
import os
from app.config import DATA_DIR

os.makedirs(DATA_DIR, exist_ok=True)

def _path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.json")

def read_json(name: str):
    path = _path(name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(name: str, data):
    with open(_path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
