import json
import os
from typing import Any

from .config import DATA_DIR

STORE_PATH = os.path.join(DATA_DIR, "documents.json")


def _load() -> list[dict[str, Any]]:
    if not os.path.exists(STORE_PATH):
        return []
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(items: list[dict[str, Any]]) -> None:
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def list_documents() -> list[dict[str, Any]]:
    return _load()


def add_document(item: dict[str, Any]) -> dict[str, Any]:
    items = _load()
    items.append(item)
    _save(items)
    return item


def get_document(doc_id: str) -> dict[str, Any] | None:
    return next((x for x in _load() if x["id"] == doc_id), None)


def delete_document(doc_id: str) -> bool:
    items = _load()
    new_items = [x for x in items if x["id"] != doc_id]
    if len(new_items) == len(items):
        return False
    _save(new_items)
    return True
