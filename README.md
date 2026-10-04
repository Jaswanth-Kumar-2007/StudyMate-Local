# StudyMate Local

A private study assistant built for a real friend who wants help understanding class notes and practicing for exams.

## Core idea

StudyMate keeps study material local and uses an open-weight LLM through Ollama for:
- Explaining topics from uploaded notes
- Answering questions using the notes as context
- Generating practice questions
- Running a short quiz

The project does not require a paid AI API.

## Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Local AI: Ollama + an open-weight model such as `qwen2.5:3b`
- Document extraction: pypdf
- Retrieval: lightweight TF-IDF retrieval implemented locally with scikit-learn

## Requirements

- Python 3.11+
- Node.js 20+
- Ollama

Install Ollama from https://ollama.com/

Then pull a model:

```bash
ollama pull qwen2.5:3b
```

You can use another Ollama model by changing `OLLAMA_MODEL` in `backend/.env`.

## Run backend

```bash
cd backend
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Run frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite, normally:

http://localhost:5173

## API

- `GET /api/health`
- `POST /api/documents`
- `GET /api/documents`
- `DELETE /api/documents/{id}`
- `POST /api/ask`
- `POST /api/explain`
- `POST /api/quiz`

## Important

This is a hackathon/weekend-challenge project. It is designed to demonstrate the open-AI/local-first idea clearly, not to replace a teacher or professional educational service.
