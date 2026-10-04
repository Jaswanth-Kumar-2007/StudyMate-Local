# StudyMate

An AI-powered study assistant built for a real friend who wants help understanding class notes and practicing for exams.

StudyMate lets students upload their study material, ask questions, understand difficult topics, and generate practice quizzes based on their own notes.

## Core Idea

StudyMate combines document retrieval with an open-weight AI model.

The application first extracts and retrieves relevant sections from uploaded study material, then provides that context to the AI model to generate an answer.

### Current Online Setup

The current online version uses **Hugging Face Inference Providers** with the open-weight:

`Qwen/Qwen3-4B-Instruct-2507`

```text
React + TypeScript
        ↓
FastAPI
        ↓
PDF extraction
        ↓
TF-IDF retrieval
        ↓
Hugging Face Inference
        ↓
Qwen3-4B-Instruct-2507
        ↓
Answer / Explanation / Quiz
```

### Local Alternative

StudyMate was initially designed around local AI inference using Ollama.

If you want to run the AI locally instead of using the online Hugging Face inference setup, Ollama can be used with an open-weight model such as `qwen2.5:3b`.

```text
React
  ↓
FastAPI
  ↓
Local retrieval
  ↓
Ollama
  ↓
Qwen
```

This makes the project flexible between cloud-based and local inference.

---

## Features

* 📄 Upload study PDFs
* 🔎 Retrieve relevant sections from uploaded material
* 💬 Ask questions about your notes
* 📚 Explain difficult topics in simpler language
* 📝 Generate practice questions
* 🧠 Generate short quizzes
* 🤖 Use an open-weight AI model
* 🌐 Run online through Hugging Face
* 💻 Option to use local inference through Ollama

---

## Tech Stack

### Frontend

* React
* TypeScript
* Vite

### Backend

* Python
* FastAPI
* Uvicorn

### AI

**Online:**

* Hugging Face Inference Providers
* Qwen/Qwen3-4B-Instruct-2507

**Local alternative:**

* Ollama
* Qwen or another compatible open-weight model

### Document Processing

* pypdf

### Retrieval

* scikit-learn
* TF-IDF retrieval

---

## Project Structure

```text
StudyMate/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── huggingface.py
│   │   ├── retrieval.py
│   │   └── store.py
│   ├── data/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.ts
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# Running StudyMate Locally

You can run the frontend and backend locally while still using Hugging Face for AI inference.

## Requirements

* Python 3.11+
* Node.js 20+
* A Hugging Face account and API token

---

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd StudyMate
```

---

## 2. Set up the backend

```bash
cd backend

python -m venv .venv
```

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Hugging Face

Create:

```text
backend/.env
```

Add:

```env
HF_TOKEN=your_huggingface_token
HF_MODEL=Qwen/Qwen3-4B-Instruct-2507

CORS_ORIGINS=http://localhost:5173
```

**Never commit your real `HF_TOKEN` to GitHub.**

The repository contains `.env.example` as a template.

---

## 4. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

## 5. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite, normally:

```text
http://localhost:5173
```

---

# Running with Ollama Instead

StudyMate can also be adapted to use local Ollama inference.

Install Ollama from:

https://ollama.com/

Then pull an open-weight model:

```bash
ollama pull qwen2.5:3b
```

The original local architecture is:

```text
PDF
 ↓
Text extraction
 ↓
TF-IDF retrieval
 ↓
Relevant context
 ↓
Ollama
 ↓
Qwen
 ↓
Study response
```

This option is useful when you want inference to happen on your own computer rather than through an online inference provider.

---

# API

| Method | Endpoint              | Purpose                             |
| ------ | --------------------- | ----------------------------------- |
| GET    | `/api/health`         | Check backend and AI configuration  |
| POST   | `/api/documents`      | Upload a study PDF                  |
| GET    | `/api/documents`      | List uploaded documents             |
| DELETE | `/api/documents/{id}` | Delete a document                   |
| POST   | `/api/ask`            | Ask a question about study material |
| POST   | `/api/explain`        | Explain a topic                     |
| POST   | `/api/quiz`           | Generate a quiz                     |

---

# How Retrieval Works

StudyMate does not simply send every uploaded document directly to the AI model.

The process is:

```text
PDF
 ↓
Extract text with pypdf
 ↓
Split text into chunks
 ↓
Create TF-IDF representation
 ↓
Find relevant chunks
 ↓
Build a context-aware prompt
 ↓
Send relevant context to Qwen
 ↓
Generate response
```

This keeps the AI focused on the student's uploaded material.

---

# Cloud Deployment

The project is designed to be deployed using:

```text
                    ┌──────────────────┐
                    │  React Frontend  │
                    │     Vercel       │
                    └────────┬─────────┘
                             │
                             ↓
                    ┌──────────────────┐
                    │ FastAPI Backend  │
                    │     Render       │
                    └────────┬─────────┘
                             │
                    PDF + Retrieval
                             │
                             ↓
                    ┌──────────────────┐
                    │    Hugging Face  │
                    │    Inference     │
                    └────────┬─────────┘
                             │
                             ↓
                    Qwen3-4B-Instruct
```

The Hugging Face API token is stored as a backend environment variable and is **never exposed to the React frontend**.

---

# Open-Source AI

StudyMate is built around an open-weight AI model rather than being tied exclusively to a proprietary closed model.

The current online AI model is:

**Qwen/Qwen3-4B-Instruct-2507**

The inference layer is provided through Hugging Face Inference Providers.

The project can also be adapted for local inference through Ollama.

This makes it possible to experiment with different models and deployment approaches without redesigning the entire application.

---

# Why I Built It

I built StudyMate for a real friend who wanted a simpler way to study from class notes.

Instead of creating another general-purpose chatbot, I wanted to make something focused on a student's actual study material.

The goal is simple:

> Upload your notes, ask questions, understand difficult topics, and test yourself.

---

# Hacktoberfest Weekend Challenge

This project was built for the **Hacktoberfest Weekend Challenge: Build for a Friend**.

The challenge encouraged participants to build something useful for a real friend or loved one while putting open-source AI at the core.

StudyMate combines:

* Open-weight AI
* Open-source software
* Document retrieval
* A real student-focused problem
* A practical AI application

---

# Security Notes

* Do not commit `.env`.
* Do not expose `HF_TOKEN` in the frontend.
* Keep API credentials in backend environment variables.
* Uploaded study material should be treated as user-provided data.
* The cloud version sends retrieved study context to the configured inference provider.

---

# Limitations

StudyMate is a hackathon/weekend project and is intentionally lightweight.

It is designed to demonstrate an AI study workflow rather than replace teachers, tutors, or professional educational services.

The retrieval system currently uses lightweight TF-IDF rather than a vector database or embedding-based retrieval system.

---

# Future Improvements

Possible future improvements include:

* Semantic embeddings for better retrieval
* Vector database integration
* Better document chunking
* Support for more document formats
* Conversation history
* User accounts
* More advanced quiz generation
* Streaming AI responses
* Additional open-weight models
* Fully local deployment with Ollama

---

## License

This project is open source. See the `LICENSE` file for details.
