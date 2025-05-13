import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load .env variables automatically

def search_syllabus(query):
    """
    Check if the query matches any question in syllabus.json
    """
    try:
        with open("syllabus.json", "r") as f:
            syllabus = json.load(f)

        for subject, topics in syllabus.items():
            for topic in topics:
                question = topic.get("question", "").lower()
                answer = topic.get("answer", "")
                if query.lower() in question:
                    return answer

    except Exception as e:
        return f"⚠️ Error loading syllabus.json: {e}"

    return None  # Return None if the query is not found in syllabus.json

def handle_greetings(query):
    """
    Check if the query is a greeting and respond accordingly.
    """
    greetings = ["hi", "hello", "hey", "howdy", "greetings"]
    if any(greeting in query.lower() for greeting in greetings):
        return "Hello! How can I assist you with your college syllabus?"

    return None  # Return None if no greeting is detected

def get_response(query):
    """
    Get the response: First check for greetings, then local syllabus, else fallback to Groq API.
    """
    # Step 1: Handle greeting queries separately
    greeting_response = handle_greetings(query)
    if greeting_response:
        return greeting_response

    # Step 2: Check local syllabus.json
    local_reply = search_syllabus(query)
    if local_reply:
        return local_reply

    # Step 3: Hit up Groq API if not found locally
    api_key = os.getenv("GROQ_API_KEY")  # Get the API key from .env
    if not api_key:
        return "❌ Missing GROQ_API_KEY in .env file"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You're a helpful college syllabus assistant. Be clear and concise."},
            {"role": "user", "content": query}
        ]
    }

    try:
        # Send request to Groq API
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for invalid responses (non-2xx)
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ Groq API error: {str(e)}"  # Return the error if the API request fails
