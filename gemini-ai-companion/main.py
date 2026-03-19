from flask import Flask, render_template, request, jsonify
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY= 'AIzaSyCx1dOggOzNSnJKhnfmGyucjqx27LXuQpw'

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(r"index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    grade = 6

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
            You are a helpful AI tutor for school children.
            Give simple, safe, age-appropriate answers.
            You are anwering the kid in grade {grade}.
            Answers should in 3 to 8 points not more than that.

            Question: {user_question}
            """
            )

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"answer": "Error contacting AI service."},e)

if __name__ == "__main__":
    app.run(debug=True)
