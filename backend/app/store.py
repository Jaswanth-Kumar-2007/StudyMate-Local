from typing import Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .config import MONGO_URI, MONGO_DB_NAME


client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]
documents_collection = db["documents"]


def list_documents() -> list[dict[str, Any]]:
    try:
        documents = list(
            documents_collection.find(
                {},
                {"_id": 0}
            )
        )

        return documents

    except PyMongoError as e:
        raise RuntimeError(f"Failed to load documents: {e}")


def add_document(item: dict[str, Any]) -> dict[str, Any]:
    try:
        documents_collection.insert_one(item)

        return item

    except PyMongoError as e:
        raise RuntimeError(f"Failed to save document: {e}")


def get_document(doc_id: str) -> dict[str, Any] | None:
    try:
        return documents_collection.find_one(
            {"id": doc_id},
            {"_id": 0}
        )

    except PyMongoError as e:
        raise RuntimeError(f"Failed to get document: {e}")


def delete_document(doc_id: str) -> bool:
    try:
        result = documents_collection.delete_one(
            {"id": doc_id}
        )

        return result.deleted_count > 0

    except PyMongoError as e:
        raise RuntimeError(f"Failed to delete document: {e}")