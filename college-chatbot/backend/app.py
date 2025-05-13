from flask import Flask, request, jsonify
from chatbot import get_response
from flask_cors import CORS  # Enable CORS for cross-origin requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

@app.route("/ask", methods=["POST"])
def ask():
    # Get the query from the frontend (JSON data sent in the body)
    data = request.get_json()
    query = data.get("query", "")  # Default to empty string if no query is provided

    if not query:
        return jsonify({"error": "No query provided"}), 400  # Return error if no query is sent

    # Fetch the response from the chatbot logic
    response = get_response(query)
    
    if "Error" in response or "❌" in response:
        return jsonify({"error": response}), 500  # Return error if there's an issue with the response

    # Send the response back to the frontend as JSON
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
