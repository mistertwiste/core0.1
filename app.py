import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai

# Umgebungsvariablen laden (.env)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_prompt(user_input: str) -> str:
    """
    Simpler 'Prompt-Generator', der das rohe Nutzer-Input
    verbessert, um bessere Antworten von GPT-4o zu bekommen.
    """
    return (
        "Bitte verbessere und erweitere dieses Prompt, damit GPT-4o "
        "die bestmögliche Antwort liefern kann:\n\n"
        f"{user_input}"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    
    # 1) Prompt optimieren
    improved_prompt = generate_prompt(user_input)

    # 2) Anfrage an OpenAI
    resp = openai.ChatCompletion.create(
        model="gpt-4o",         # dein Modell
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": improved_prompt}
        ]
    )
    answer = resp.choices[0].message.content.strip()

    # 3) Antwort zurück an den Browser
    return jsonify({"answer": answer})

if __name__ == "__main__":
    # Für die Entwicklung: http://127.0.0.1:5000
    app.run(debug=True)
