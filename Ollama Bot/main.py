from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

def generate_response(user_input):
    prompt = f"""
You are a friendly educational AI for children aged 8-15.
Use simple and professional words.
Keep answers short (max 4 sentences).
Never discuss adult topics.
Be encouraging and positive.

Question: {user_input}
Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 100
            }
        }
    )

    return response.json()["response"]

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"]
    reply = generate_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
