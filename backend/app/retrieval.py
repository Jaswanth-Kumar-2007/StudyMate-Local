import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MAX_CHUNK = 1200


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str) -> list[str]:
    text = clean(text)
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + MAX_CHUNK, len(text))
        if end < len(text):
            boundary = text.rfind(". ", start, end)
            if boundary > start + 400:
                end = boundary + 1
        chunks.append(text[start:end].strip())
        start = end
    return [c for c in chunks if c]


def retrieve(question: str, documents: list[dict], top_k: int = 5) -> list[dict]:
    corpus = []
    metadata = []

    for doc in documents:
        for chunk in doc.get("chunks", []):
            corpus.append(chunk)
            metadata.append({
                "document_id": doc["id"],
                "document_name": doc["name"],
                "text": chunk,
            })

    if not corpus:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()

    ranked = scores.argsort()[::-1][:top_k]
    results = []
    for idx in ranked:
        if scores[idx] <= 0:
            continue
        item = dict(metadata[idx])
        item["score"] = float(scores[idx])
        results.append(item)
    return results
