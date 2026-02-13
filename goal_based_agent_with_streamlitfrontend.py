import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import re
import fitz

load_dotenv()


llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Global storage for application info
application_info = {"name": None, "email": None, "skills": None}

# Extract info from plain text (chat or resume)
def extract_application_info(text: str) -> str:
    name_match = re.search(r"(?:my name is|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text, re.IGNORECASE)
    email_match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    skills_match =re.search(r"(?:skills\s*:?\s*|skills are\s+|i know\s+|i can use\s+)(.+)", text, re.IGNORECASE)

    if name_match:
        application_info["name"] = name_match.group(1).title()
    if email_match:
        application_info["email"] = email_match.group(0)
    if skills_match:
        application_info["skills"] = skills_match.group(1).strip()

    return "Got it. Let me check what else I need."

# Extract info from uploaded CV
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_info_from_cv(text: str):
    extracted_info = {"name": None, "email": None, "skills": None}

    # EMAIL (strong detection)
    email_match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    if email_match:
        extracted_info["email"] = email_match.group(0)

    # NAME (first non-empty line)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        if len(first_line.split()) <= 4:
            extracted_info["name"] = first_line

    # SKILLS (more flexible)
    skills_section = re.search(r"skills[:\s]*(.*)", text, re.IGNORECASE)
    if skills_section:
        extracted_info["skills"] = skills_section.group(1).strip()

    return extracted_info


# Goal checker
def check_application_goal(_: str) -> str:
    if all(application_info.values()):
        return f"✅ You're ready! Name: {application_info['name']}, Email: {application_info['email']}, Skills: {application_info['skills']}."
    else:
        missing = [k for k, v in application_info.items() if not v]
        return f"⏳ Still need: {', '.join(missing)}"

# Define tools for LangChain agent
tools = [
    Tool(name="extract_application_info", func=extract_application_info, description="Extract name, email, skills"),
    Tool(name="check_application_goal", func=check_application_goal, description="Check completion")
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False
)

# Streamlit UI
st.set_page_config(page_title="🎯 Job Application Assistant", layout="centered")
st.title("🧠 Goal-Based Agent: Job Application Assistant")
st.markdown("Tell me your **name**, **email**, and **skills** to complete your application!")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "goal_complete" not in st.session_state:
    st.session_state.goal_complete = False
if "download_ready" not in st.session_state:
    st.session_state.download_ready = False
if "application_summary" not in st.session_state:
    st.session_state.application_summary = ""

# Upload resume
st.sidebar.header("📤 Upload Resume (Optional)")
resume = st.sidebar.file_uploader("Upload your resume", type=["pdf", "txt"])

if resume:
    st.sidebar.success("Resume uploaded!")
    text = extract_text_from_pdf(resume)
    extracted = extract_info_from_cv(text)
    for key in application_info:
        if extracted[key]:
            application_info[key] = extracted[key]
    st.sidebar.info("🔍 Extracted info from resume:")
    for key, value in extracted.items():
        st.sidebar.markdown(f"**{key.capitalize()}:** {value}")

# Reset chat
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.chat_history.clear()
    st.session_state.goal_complete = False
    st.session_state.download_ready = False
    st.session_state.application_summary = ""
    for key in application_info:
        application_info[key] = None
    st.rerun()


# Chat input
user_input = st.chat_input("Type here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    extract_application_info(user_input)
    response = agent.invoke({"input": user_input})
    bot_reply = response["output"]
    st.session_state.chat_history.append(("bot", bot_reply))
    goal_status = check_application_goal("check")
    st.session_state.chat_history.append(("status", goal_status))

    if "you're ready" in goal_status.lower():
        st.session_state.goal_complete = True
        summary = (
            f"✅ Name: {application_info['name']}\n"
            f"📧 Email: {application_info['email']}\n"
            f"🛠️ Skills: {application_info['skills']}\n"
        )
        st.session_state.application_summary = summary
        st.session_state.download_ready = True

# Chat UI with avatars
for sender, message in st.session_state.chat_history:
    if sender == "user":
        with st.chat_message("🧑"):
            st.markdown(message)
    elif sender == "bot":
        with st.chat_message("🤖"):
            st.markdown(message)
    elif sender == "status":
        with st.chat_message("📊"):
            st.info(message)

# Final message
if st.session_state.goal_complete:
    st.success("🎉 All information collected! You're ready to apply!")

# Download summary
if st.session_state.download_ready:
    st.download_button(
        label="📥 Download Application Summary",
        data=st.session_state.application_summary,
        file_name="application_summary.txt",
        mime="text/plain"
    )