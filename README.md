# StudyMate

> An AI-powered study companion that helps students understand their own notes, ask questions, and practice for exams.

StudyMate was built for a real friend who wanted a simple way to understand class notes and prepare for exams.

Instead of searching through long PDFs manually, students can upload their notes and use StudyMate to ask questions, learn difficult topics, and generate practice quizzes from the uploaded material.

---

## ✨ Features

- 📄 Upload PDF study notes
- 🔎 Retrieve relevant sections from uploaded notes
- 💬 Ask questions about your notes
- 🧠 Get simple explanations of difficult topics
- 📝 Generate multiple-choice practice quizzes
- 🗑️ Manage and delete uploaded documents
- 📚 View document pages and extracted sections
- 🤖 Open-weight AI at the core
- 🖥️ Local AI option using Ollama
- ☁️ Online AI inference using Hugging Face
- 🗄️ MongoDB persistence for uploaded document data
- ⚡ Upload processing feedback so users know when their PDF is being processed

---

## 🏗️ How It Works

### Online Version

The currently deployed version uses Hugging Face for AI inference.

```text
React + TypeScript + Vite
            ↓
        FastAPI
            ↓
     PDF text extraction
            ↓
     TF-IDF retrieval
            ↓
   Relevant study sections
            ↓
 Hugging Face Inference
            ↓
Qwen/Qwen3-4B-Instruct-2507
````

MongoDB Atlas stores the extracted document data and chunks.

### Local AI Version

StudyMate can also be run with a local AI model using Ollama:

```text
React
  ↓
FastAPI
  ↓
PDF extraction
  ↓
TF-IDF retrieval
  ↓
Ollama
  ↓
Qwen 2.5 3B
```

This provides an alternative where AI inference can happen on the user's own machine.

---

## 🧰 Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Lucide React
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* pypdf
* scikit-learn

### AI

**Online:**

* Hugging Face Inference Providers
* `Qwen/Qwen3-4B-Instruct-2507`

**Local:**

* Ollama
* `qwen2.5:3b`

### Database

* MongoDB Atlas
* PyMongo

### Deployment

* Render

---

## 📂 Project Structure

```text
StudyMate/
│
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── huggingface.py
│   │   ├── main.py
│   │   ├── retrieval.py
│   │   └── store.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── App.css
│   │   └── vite-env.d.ts
│   │
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# 🚀 Running Locally

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd StudyMate
```

---

## 2. Backend Setup

```bash
cd backend
```

Create a virtual environment:

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a file:

```text
backend/.env
```

For the Hugging Face setup:

```env
HF_TOKEN=your_huggingface_token
HF_MODEL=Qwen/Qwen3-4B-Instruct-2507

MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=studymate

CORS_ORIGINS=http://localhost:5173
```

Never commit your `.env` file or API tokens to GitHub.

---

# 🖥️ Local Ollama Setup

If you want to run AI inference locally instead of using Hugging Face, install Ollama and download an open-weight model such as:

```text
qwen2.5:3b
```

The local Ollama configuration can then be used for local inference.

This provides an alternative for users who want the AI inference component to run on their own machine.

---

# ▶️ Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# ▶️ Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

If you want the frontend to use the deployed backend, configure:

```env
VITE_API_URL=https://studymate-local.onrender.com/api
```

---

# 🔌 API Endpoints

| Method | Endpoint              | Purpose                 |
| ------ | --------------------- | ----------------------- |
| GET    | `/api/health`         | Check backend health    |
| GET    | `/api/documents`      | List uploaded documents |
| POST   | `/api/documents`      | Upload a PDF            |
| DELETE | `/api/documents/{id}` | Delete a document       |
| POST   | `/api/ask`            | Ask a question          |
| POST   | `/api/explain`        | Explain a topic         |
| POST   | `/api/quiz`           | Generate a quiz         |

---

# 🔎 Retrieval Pipeline

StudyMate does not simply send the entire document to the AI model.

The application first:

1. Extracts text from the uploaded PDF.
2. Splits the text into smaller chunks.
3. Uses TF-IDF to identify relevant chunks.
4. Selects the most relevant study sections.
5. Sends those sections as context to the AI model.
6. Generates an answer based on the retrieved notes.

This keeps the AI focused on the student's own study material.

---

# 🤖 Why Open-Weight AI?

Open innovation gives developers the ability to experiment, build, and modify applications using openly available technologies rather than depending entirely on closed systems.

StudyMate uses the open-weight Qwen model as its AI foundation.

The deployed version uses Hugging Face for inference, while the project also supports Ollama for local model execution.

This flexibility allows developers to:

* Experiment with different models
* Run models locally
* Learn how AI systems work
* Build applications without being locked into a single AI provider
* Combine open-source software with open-weight AI

---

# ❤️ Built for a Friend

StudyMate was created for a real friend who needed help understanding class notes and preparing for exams.

The goal was not to build another general-purpose chatbot.

The goal was to solve a specific problem:

> "I have my notes, but I don't want to spend hours searching through them to understand what I need for my exam."

That led to the core workflow:

```text
Upload notes
     ↓
Ask about the notes
     ↓
Understand difficult topics
     ↓
Practice with quizzes
```

The application was designed around that actual use case rather than simply adding AI features for the sake of using AI.

---

# 🔐 Security & Privacy

* API tokens are stored in environment variables.
* Secrets should never be committed to GitHub.
* The Hugging Face token is kept on the backend and is not exposed to the frontend.
* MongoDB credentials are stored in environment variables.

### Important Privacy Note

The deployed version uses Hugging Face for AI inference. Therefore, relevant retrieved study-note context is sent to the configured Hugging Face inference service.

The local Ollama setup provides an alternative for users who want AI inference to happen on their own machine.

---

# ⚠️ Current Limitations

StudyMate is a hackathon project and intentionally uses a lightweight retrieval system.

Current limitations include:

* TF-IDF retrieval is simpler than modern embedding-based retrieval.
* PDF extraction depends on selectable text.
* Scanned/image-only PDFs are not currently supported.
* The application does not yet provide user accounts.
* Conversation history is not persistent.
* Quiz quality depends on the quality of the retrieved notes.
* The deployed AI inference depends on the availability of the inference provider.

---

# 🔮 Future Improvements

Possible future improvements include:

* Semantic embeddings
* Vector database retrieval
* Better document chunking
* OCR for scanned PDFs
* Support for more document formats
* Persistent conversation history
* User authentication
* Streaming AI responses
* More local model options
* Better quiz evaluation
* Personalized study plans

---

# 🏆 Hacktoberfest Weekend Challenge

StudyMate was built for the **Build for a Friend** challenge.

The project focuses on a real student problem while keeping open-source software and open-weight AI at the core.

The goal was to combine open technologies with a practical application that could actually help someone in their everyday studies.

---

# 📜 License

Add your chosen open-source license here.

---

# 👨‍💻 Author

**Jaswanth Kumar**

````


