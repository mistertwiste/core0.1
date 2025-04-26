import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
import streamlit as st

# 1. API-Key laden
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
client = OpenAI(api_key=api_key)

# 2. Prompt-Generator
def generate_prompt(user_input: str) -> str:
    return (
        "Bitte verbessere und erweitere dieses Prompt, damit GPT-4o "
        "die bestmögliche Antwort liefern kann:\n\n"
        f"{user_input}"
    )

# 3. Streamlit-UI
st.set_page_config(page_title="GPT-4o Chat MVP")
st.title("GPT-4o Chat MVP")

# Session-State für Chat-Verlauf initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eingabeformular
with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input("Deine Nachricht:")
    send = st.form_submit_button("Senden")

# Bei Klick auf „Senden“:
if send and user_text:
    # 3.1 Nutzer-Nachricht speichern
    st.session_state.messages.append({"role": "user", "content": user_text})

    # 3.2 Prompt optimieren
    prompt = generate_prompt(user_text)

    # 3.3 Anfrage an OpenAI (neue API-Client-Syntax)
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user",   "content": prompt},
        ],
    )

    # 3.4 Antwort extrahieren und speichern
    answer = resp.choices[0].message.content.strip()
    st.session_state.messages.append({"role": "assistant", "content": answer})

# 4. Chat-Verlauf rendern
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align: right; color: blue;'><strong>Du:</strong> {msg['content']}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align: left; color: green;'><strong>Bot:</strong> {msg['content']}</div>",
            unsafe_allow_html=True,
        )
