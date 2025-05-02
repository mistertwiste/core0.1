# core_app.py

import streamlit as st
import os
import json
import openai

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize session state for goals, tasks, and chat
if "goals" not in st.session_state:
    st.session_state.goals = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# Functions
# ----------------------------
def add_goal(title, description, milestones_tasks):
    st.session_state.goals.append({
        "title": title,
        "description": description,
        "milestones": milestones_tasks
    })

def display_goals():
    for idx, goal in enumerate(st.session_state.goals):
        with st.expander(f"{goal['title']}"):
            st.markdown(f"**Description:** {goal['description']}")
            for ms_idx, milestone in enumerate(goal['milestones']):
                st.markdown(f"- Milestone {ms_idx+1}: {milestone['milestone']}")
                for task in milestone['tasks']:
                    st.markdown(f"    - [ ] {task}")

def handle_chat(user_input):
    # Construct context from goals
    context = "\n".join([
        f"Goal: {g['title']}, Description: {g['description']}" for g in st.session_state.goals
    ])
    
    prompt = f"You are a productivity assistant. Based on the user's goals below, respond helpfully.\n\n{context}\n\nUser: {user_input}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You help users stay productive and plan effectively."},
            {"role": "user", "content": prompt}
        ]
    )
    ai_response = response.choices[0].message['content']
    st.session_state.chat_history.append((user_input, ai_response))

# ----------------------------
# UI Layout
# ----------------------------
st.set_page_config(page_title="CORE - AI Productivity Workspace", layout="wide")

st.sidebar.title("🧠 CORE")
st.title("CORE MVP - Goal Tracker & AI Assistant")

# Input Form for New Goal
with st.form("new_goal_form"):
    st.subheader("➕ Add New Goal")
    goal_title = st.text_input("Goal Title")
    goal_desc = st.text_area("Goal Description")

    milestone_count = st.number_input("How many milestones?", min_value=1, max_value=10, value=1)
    milestones_tasks = []

    for i in range(int(milestone_count)):
        st.markdown(f"**Milestone {i+1}**")
        milestone_title = st.text_input(f"Milestone {i+1} Title", key=f"ms_{i}")
        tasks = st.text_area(f"Tasks for Milestone {i+1} (comma separated)", key=f"tasks_{i}")
        task_list = [t.strip() for t in tasks.split(",") if t.strip() != ""]
        milestones_tasks.append({"milestone": milestone_title, "tasks": task_list})

    submitted = st.form_submit_button("Add Goal")
    if submitted and goal_title:
        add_goal(goal_title, goal_desc, milestones_tasks)
        st.success("Goal added successfully!")

# Display Active Goals
st.subheader("📌 My Goals")
display_goals()

# Chat Assistant Section
st.subheader("💬 AI Assistant")
user_message = st.text_input("Ask your assistant something:")
if st.button("Send") and user_message:
    handle_chat(user_message)

# Show chat history
for user_input, response in st.session_state.chat_history:
    st.markdown(f"**You:** {user_input}")
    st.markdown(f"**CORE AI:** {response}")

# Export Goals as JSON
st.subheader("📁 Export Goals")
if st.button("Download JSON"):
    goals_json = json.dumps(st.session_state.goals, indent=2)
    st.download_button("Download Goals JSON", goals_json, file_name="core_goals.json")
