import React from "react";

function ChatBox({ query, response }) {
  return (
    <div className="response-box">
      <h3>Your Query:</h3>
      <p>{query}</p>
      <h3>Response:</h3>
      <p>{response}</p>
    </div>
  );
}

export default ChatBox;
