import React, { useState } from "react";
import ChatBox from "./ChatBox";
import "./styles.css";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("https://ideal-space-system-4j7p94rj6rqgcq4px-5000.app.github.dev/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="container">
      <h1>Deshik Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
        />
        <button type="submit">Ask</button>
      </form>
      {response && <ChatBox query={query} response={response} />}
    </div>
  );
}

export default App;
