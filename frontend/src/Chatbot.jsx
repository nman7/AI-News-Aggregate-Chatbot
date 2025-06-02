import React, { useState } from "react";

const Chatbot = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat-query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 3 }),
      });

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error("❌ Error:", err);
      alert("Failed to fetch chatbot results.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>🧠 Ask NewsBot</h2>
      <form onSubmit={handleQuerySubmit}>
        <input
          type="text"
          value={query}
          placeholder="Ask a question like: 'What happened in State of Origin?'"
          onChange={(e) => setQuery(e.target.value)}
          style={{ padding: "8px", width: "70%" }}
        />
        <button type="submit" style={{ marginLeft: "10px", padding: "8px" }}>
          Ask
        </button>
      </form>

      {loading && <p>🔄 Searching...</p>}

      {results.length > 0 && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Top Answers</h3>
          <ul>
            {results.map((item, idx) => (
              <li key={idx} style={{ marginBottom: "1rem" }}>
                <strong>{item.title}</strong>
                <p>{item.summary}</p>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  Read more →
                </a>
                <p>
                  <small>
                    Source: {item.source} | Category: {item.category}
                  </small>
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
