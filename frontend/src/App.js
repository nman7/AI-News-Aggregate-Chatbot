import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [highlights, setHighlights] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/highlights")
      .then(res => setHighlights(res.data))
      .catch(err => console.error("Failed to fetch highlights", err));
  }, []);

  return (
    <div>
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
    </div>
  );
}

export default App;
