import { useEffect, useState } from "react";
import {
  BookOpen,
  Brain,
  FileText,
  GraduationCap,
  MessageCircle,
  Plus,
  Send,
  Sparkles,
  Trash2,
  Trophy,
  Upload,
  X,
} from "lucide-react";

const API =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

type Document = {
  id: string;
  name: string;
  pages: number;
  chunks: number;
};

type QuizQuestion = {
  question: string;
  options: string[];
  answer: number;
  explanation: string;
};

type Quiz = {
  questions: QuizQuestion[];
};

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [active, setActive] = useState<"ask" | "explain" | "quiz">("ask");
  const [question, setQuestion] = useState("");
  const [topic, setTopic] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [quizIndex, setQuizIndex] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [score, setScore] = useState(0);

  const loadDocuments = async () => {
    const res = await fetch(`${API}/documents`);
    if (res.ok) setDocuments(await res.json());
  };

  useEffect(() => {
    loadDocuments().catch(() => {});
  }, []);

  const upload = async (file: File) => {
    setError("");
    const form = new FormData();
    form.append("file", file);

    const res = await fetch(`${API}/documents`, {
      method: "POST",
      body: form,
    });

    const data = await res.json();
    if (!res.ok) {
      setError(data.detail || "Upload failed.");
      return;
    }
    await loadDocuments();
  };

  const remove = async (id: string) => {
    await fetch(`${API}/documents/${id}`, { method: "DELETE" });
    await loadDocuments();
  };

  const runAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const res = await fetch(`${API}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Request failed.");
      setAnswer(data.answer);
      setSources(data.sources?.map((x: { name: string }) => x.name) || []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const runExplain = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const res = await fetch(`${API}/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Request failed.");
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const runQuiz = async () => {
    setLoading(true);
    setError("");
    setQuiz(null);
    setQuizIndex(0);
    setSelected(null);
    setScore(0);

    try {
      const res = await fetch(`${API}/quiz`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, count: 5 }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Quiz generation failed.");
      setQuiz(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = () => {
    if (!quiz || selected === null) return;

    const correct = selected === quiz.questions[quizIndex].answer;
    const newScore = score + (correct ? 1 : 0);

    if (quizIndex < quiz.questions.length - 1) {
      setScore(newScore);
      setQuizIndex((i) => i + 1);
      setSelected(null);
    } else {
      setScore(newScore);
      setSelected(selected);
    }
  };

  const hasFinished = quiz && quizIndex === quiz.questions.length - 1 && selected !== null;

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon"><GraduationCap size={22} /></div>
          <div>
            <strong>StudyMate</strong>
            <span>Local AI Study Partner</span>
          </div>
        </div>
        <div className="privacy-pill"><span /> Runs locally</div>
      </header>

      <main className="layout">
        <aside className="sidebar">
          <div className="sidebar-title">
            <span>Your Notes</span>
            <label className="upload-btn">
              <Plus size={17} />
              <input
                type="file"
                accept=".pdf"
                hidden
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) upload(file);
                  e.currentTarget.value = "";
                }}
              />
            </label>
          </div>

          <label className="dropzone">
            <Upload size={20} />
            <b>Upload PDF notes</b>
            <span>Your files stay on this machine.</span>
            <input
              type="file"
              accept=".pdf"
              hidden
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) upload(file);
                e.currentTarget.value = "";
              }}
            />
          </label>

          <div className="doc-list">
            {documents.length === 0 ? (
              <div className="empty-docs">
                <FileText size={22} />
                <span>No notes yet</span>
              </div>
            ) : documents.map((doc) => (
              <div className="doc" key={doc.id}>
                <FileText size={18} />
                <div className="doc-info">
                  <b>{doc.name}</b>
                  <span>{doc.pages} pages · {doc.chunks} sections</span>
                </div>
                <button onClick={() => remove(doc.id)} title="Delete">
                  <Trash2 size={15} />
                </button>
              </div>
            ))}
          </div>

          <div className="privacy-card">
            <Sparkles size={18} />
            <b>Private by design</b>
            <p>Your study material is processed by your local AI setup instead of being sent to a paid AI API.</p>
          </div>
        </aside>

        <section className="content">
          <div className="hero">
            <span className="eyebrow">BUILT FOR A FRIEND</span>
            <h1>Study smarter.<br /><em>Keep your notes private.</em></h1>
            <p>Ask questions, understand difficult topics, and practice from your own notes with an open-weight AI model running locally.</p>
          </div>

          <div className="tabs">
            <button className={active === "ask" ? "active" : ""} onClick={() => setActive("ask")}>
              <MessageCircle size={18} /> Ask
            </button>
            <button className={active === "explain" ? "active" : ""} onClick={() => setActive("explain")}>
              <Brain size={18} /> Explain
            </button>
            <button className={active === "quiz" ? "active" : ""} onClick={() => setActive("quiz")}>
              <Trophy size={18} /> Quiz
            </button>
          </div>

          <div className="panel">
            {active === "ask" && (
              <>
                <div className="panel-heading">
                  <div className="round-icon"><MessageCircle /></div>
                  <div>
                    <h2>Ask your notes</h2>
                    <p>StudyMate retrieves relevant sections before asking the local model.</p>
                  </div>
                </div>
                <div className="input-row">
                  <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="e.g. Explain linked lists in simple terms..."
                    rows={3}
                  />
                  <button className="primary" onClick={runAsk} disabled={loading || !question.trim()}>
                    <Send size={17} /> {loading ? "Thinking..." : "Ask"}
                  </button>
                </div>
              </>
            )}

            {active === "explain" && (
              <>
                <div className="panel-heading">
                  <div className="round-icon"><Brain /></div>
                  <div>
                    <h2>Teach me a topic</h2>
                    <p>Get a simple explanation, analogy, key points, and exam tips.</p>
                  </div>
                </div>
                <div className="input-row single">
                  <input
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g. TCP congestion control"
                  />
                  <button className="primary" onClick={runExplain} disabled={loading || !topic.trim()}>
                    <Sparkles size={17} /> {loading ? "Teaching..." : "Explain"}
                  </button>
                </div>
              </>
            )}

            {active === "quiz" && (
              <>
                <div className="panel-heading">
                  <div className="round-icon"><Trophy /></div>
                  <div>
                    <h2>Practice quiz</h2>
                    <p>Generate five multiple-choice questions from your notes.</p>
                  </div>
                </div>
                {!quiz ? (
                  <div className="quiz-start">
                    <input
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                      placeholder="Optional topic, e.g. DBMS"
                    />
                    <button className="primary" onClick={runQuiz} disabled={loading || documents.length === 0}>
                      <Trophy size={17} /> {loading ? "Creating quiz..." : "Create quiz"}
                    </button>
                    {documents.length === 0 && <span>Upload at least one PDF first.</span>}
                  </div>
                ) : (
                  <div className="quiz-box">
                    <div className="quiz-meta">Question {quizIndex + 1} of {quiz.questions.length}</div>
                    <h3>{quiz.questions[quizIndex].question}</h3>
                    <div className="options">
                      {quiz.questions[quizIndex].options.map((option, i) => (
                        <button
                          key={option}
                          className={selected === i ? "selected" : ""}
                          onClick={() => setSelected(i)}
                        >
                          <span>{String.fromCharCode(65 + i)}</span>{option}
                        </button>
                      ))}
                    </div>
                    <button className="primary" disabled={selected === null} onClick={submitAnswer}>
                      {hasFinished ? "Finish quiz" : "Next question"}
                    </button>
                    {hasFinished && (
                      <div className="score">
                        <strong>Quiz complete!</strong>
                        <span>Your score: {score}/{quiz.questions.length}</span>
                        <button onClick={() => setQuiz(null)}>Try another quiz</button>
                      </div>
                    )}
                  </div>
                )}
              </>
            )}
          </div>

          {error && <div className="error"><X size={18} />{error}</div>}

          {answer && (
            <div className="answer-card">
              <div className="answer-header">
                <div><Sparkles size={18} /><b>StudyMate's answer</b></div>
                {sources.length > 0 && <span>{sources.length} source{sources.length > 1 ? "s" : ""}</span>}
              </div>
              <div className="answer-text">{answer}</div>
              {sources.length > 0 && (
                <div className="sources">
                  {sources.map((s) => <span key={s}><BookOpen size={13} /> {s}</span>)}
                </div>
              )}
            </div>
          )}
        </section>
      </main>

      <footer>
        <span>StudyMate Local</span>
        <span>Open-weight AI · Local inference · Private study notes</span>
      </footer>
    </div>
  );
}

export default App;
