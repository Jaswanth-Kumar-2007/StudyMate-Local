import os
import tempfile
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pypdf import PdfReader

from .config import CORS_ORIGINS
from .huggingface import generate
from .retrieval import chunk_text, retrieve
from .store import add_document, delete_document, list_documents

app = FastAPI(title="StudyMate Local API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=500)


class QuizRequest(BaseModel):
    topic: str = Field(default="", max_length=500)
    count: int = Field(default=5, ge=1, le=10)


def all_context():
    return list_documents()


def format_context(results: list[dict]) -> str:
    if not results:
        return "No matching study notes were found."
    return "\n\n".join(
        f"[Source: {r['document_name']}]\n{r['text']}"
        for r in results
    )


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "ai_provider": "huggingface",
        "model": "Qwen/Qwen3-4B-Instruct-2507",
    }


@app.get("/api/documents")
def documents():
    docs = list_documents()
    return [
        {
            "id": d["id"],
            "name": d["name"],
            "pages": d.get("pages", 0),
            "chunks": len(d.get("chunks", [])),
        }
        for d in docs
    ]


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    raw = await file.read()

    try:
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        with open(temp_path, "wb") as f:
            f.write(raw)

        reader = PdfReader(temp_path)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        text = "\n".join(pages)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No selectable text was found in this PDF."
        )

    item = {
        "id": str(uuid.uuid4()),
        "name": file.filename,
        "pages": len(reader.pages),
        "chunks": chunks,
    }
    add_document(item)

    return {
        "id": item["id"],
        "name": item["name"],
        "pages": item["pages"],
        "chunks": len(chunks),
    }


@app.delete("/api/documents/{doc_id}")
def remove_document(doc_id: str):
    if not delete_document(doc_id):
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"message": "Document deleted."}


@app.post("/api/ask")
def ask(request: AskRequest):
    results = retrieve(request.question, all_context())

    prompt = f"""You are StudyMate, a patient study tutor.

Answer the student's question using ONLY the supplied study notes when possible.
If the notes do not contain enough information, clearly say that the notes do not
contain enough information instead of inventing facts.

Explain in simple language suitable for a college student.
Use short sections and bullet points when useful.

STUDY NOTES:
{format_context(results)}

STUDENT QUESTION:
{request.question}
"""
    try:
        answer = generate(prompt)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not reach the Hugging Face model. Details: {exc}"
        )

    return {
        "answer": answer,
        "sources": [
            {"name": r["document_name"], "score": round(r["score"], 3)}
            for r in results
        ],
    }


@app.post("/api/explain")
def explain(request: ExplainRequest):
    results = retrieve(request.topic, all_context())
    prompt = f"""You are StudyMate, an exam-preparation tutor.

Teach the topic below using the study notes as your primary source.

Topic: {request.topic}

Notes:
{format_context(results)}

Give:
1. A simple explanation
2. The key ideas to remember
3. One small real-world/example analogy
4. Three exam points

Do not make up details that conflict with the notes.
"""
    try:
        answer = generate(prompt)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Ollama error: {exc}")

    return {"answer": answer, "sources": [r["document_name"] for r in results]}


@app.post("/api/quiz")
def quiz(request: QuizRequest):
    query = request.topic or "main concepts"
    results = retrieve(query, all_context(), top_k=8)

    prompt = f"""Create a short study quiz from the supplied notes.

Topic: {request.topic or "all available notes"}
Number of questions: {request.count}

Return ONLY valid JSON in this shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "answer": 0,
      "explanation": "string"
    }}
  ]
}}

Rules:
- answer is the zero-based index of the correct option.
- Questions must be answerable from the notes.
- Do not invent facts.
- Keep questions useful for exam practice.

NOTES:
{format_context(results)}
"""
    try:
        raw = generate(prompt, temperature=0.1)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Ollama error: {exc}")

    import json
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1:
            raise HTTPException(status_code=500, detail="Model returned invalid quiz JSON.")
        try:
            data = json.loads(raw[start:end + 1])
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Model returned invalid quiz JSON.")

    return data
