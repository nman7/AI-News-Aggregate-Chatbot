import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [highlights, setHighlights] = useState([]);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get("http://localhost:8000/api/highlights")
      .then(res => setHighlights(res.data))
      .catch(err => console.error("Failed to fetch highlights", err));
  }, []);

  const askQuestion = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const res = await axios.post("http://localhost:8000/api/chat-query", {
        query,
        top_k: 3,
      });

      setAnswer(res.data.answer);
      setSources(res.data.sources || []);
    } catch (err) {
      setAnswer("❌ Error: Could not fetch answer.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "Inter, sans-serif", background: "#f9fafb", padding: "1rem" }}>
      <h1 style={{
        textAlign: "center",
        fontSize: "2rem",
        color: "#1f2937",
        marginBottom: "1.5rem"
      }}>🗞️ AI-Powered News Highlights</h1>

      <div style={{
        display: "flex",
        flexDirection: "column-reverse",
        gap: "2rem",
        alignItems: "stretch"
      }}>
        {/* LEFT: Highlights */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "1.5rem"
        }}>
          {highlights.map((item, index) => (
            <div key={index} style={{
              background: "#fff",
              padding: "1rem",
              borderRadius: "12px",
              boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
              border: "1px solid #e5e7eb"
            }}>
              <h3 style={{ fontSize: "1.1rem", color: "#111827", marginBottom: "0.5rem" }}>{item.title}</h3>
              <p style={{ fontStyle: "italic", fontSize: "0.95rem", color: "#4b5563" }}>{item.summary}</p>
              <a href={item.url} target="_blank" rel="noreferrer" style={{ color: "#2563eb" }}>Read more</a>
              <div style={{ fontSize: "0.85rem", marginTop: "0.5rem", color: "#6b7280" }}>
                <strong>Category:</strong> {item.category}<br />
                <strong>Sources:</strong> {item.sources.join(", ")}<br />
                <strong>Frequency:</strong> {item.frequency}
              </div>
            </div>
          ))}
        </div>

        {/* RIGHT: Chatbot */}
        <div style={{
          background: "#fff",
          padding: "1.5rem",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
          border: "1px solid #e5e7eb",
          maxWidth: "100%",
        }}>
          <h2 style={{ fontSize: "1.4rem", color: "#1f2937", marginBottom: "1rem" }}>🤖 Ask the News Bot</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Why did Glenn Maxwell retire?"
              style={{
                padding: "0.6rem 0.8rem",
                borderRadius: "8px",
                border: "1px solid #d1d5db",
                fontSize: "1rem"
              }}
            />
            <button
              onClick={askQuestion}
              style={{
                padding: "0.6rem 1.2rem",
                backgroundColor: "#2563eb",
                color: "#fff",
                fontSize: "1rem",
                borderRadius: "8px",
                border: "none",
                cursor: "pointer",
                width: "fit-content"
              }}
            >
              Ask
            </button>
          </div>

          {loading && <p style={{ marginTop: "1rem", color: "#6b7280" }}>🔄 Thinking...</p>}

          {answer && (
            <div style={{ marginTop: "1rem" }}>
              <h3>🧠 Answer:</h3>
              <p style={{ color: "#374151", fontSize: "1rem" }}>{answer}</p>
            </div>
          )}

          {sources.length > 0 && (
            <div style={{ marginTop: "1.5rem" }}>
              <h4>📚 Sources:</h4>
              <ul style={{ paddingLeft: "1rem", color: "#4b5563", fontSize: "0.95rem" }}>
                {sources.map((src, index) => (
                  <li key={index} style={{ marginBottom: "0.5rem" }}>
                    <a href={src.url} target="_blank" rel="noreferrer" style={{ color: "#2563eb" }}>{src.title}</a><br />
                    <em>{src.category}</em>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
