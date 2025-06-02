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
        query: query,
        top_k: 3
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
    <div style={{ padding: "2rem" }}>
      <h1>📰 Daily Highlights</h1>
      <ul>
        {highlights.map((item, index) => (
          <li key={index}>
            <strong>{item.title}</strong><br />
            <em>{item.summary}</em><br />
            <a href={item.url} target="_blank" rel="noreferrer">Read more</a><br />
            Sources: {item.sources.join(", ")} | Frequency: {item.frequency}
            <hr />
          </li>
        ))}
      </ul>

      <div style={{ marginTop: "2rem" }}>
        <h2>🤖 Ask the News Bot</h2>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something about the news..."
          style={{ width: "60%", padding: "0.5rem" }}
        />
        <button onClick={askQuestion} style={{ marginLeft: "1rem", padding: "0.5rem 1rem" }}>
          Ask
        </button>

        {loading && <p>🔄 Thinking...</p>}

        {answer && (
          <>
            <h3>🧠 Answer:</h3>
            <p>{answer}</p>
          </>
        )}

        {sources.length > 0 && (
          <>
            <h4>📚 Sources:</h4>
            <ul>
              {sources.map((src, index) => (
                <li key={index}>
                  <a href={src.url} target="_blank" rel="noreferrer">{src.title}</a><br />
                  <em>{src.category}</em>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
