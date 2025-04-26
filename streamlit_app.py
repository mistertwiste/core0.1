import os
from dotenv import load_dotenv
import openai
import streamlit as st

# 1. API-Key laden
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2. Prompt-Generator
def generate_prompt(user_input: str) -> str:
    return (
        "Bitte verbessere und erweitere dieses Prompt, damit GPT-4o "
        "die bestmögliche Antwort liefern kann:\n\n"
        f"{user_input}"
    )

# 3. Streamlit UI
st.set_page_config(page_title="GPT-4o Chat MVP")
st.title("GPT-4o Chat MVP")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Eingabefeld + Senden-Button
with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input("Deine Nachricht:")
    send = st.form_submit_button("Senden")

if send and user_text:
    # Nachricht in Session speichern
    st.session_state.messages.append({"role": "user", "content": user_text})

    # Prompt optimieren
    prompt = generate_prompt(user_text)

    # OpenAI-Call
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": prompt},
        ],
    )
    answer = resp.choices[0].message.content.strip()
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Chat-Anzeige
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align: right; color: blue;'>**Du:** {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color: green;'>**Bot:** {msg['content']}</div>", unsafe_allow_html=True)
