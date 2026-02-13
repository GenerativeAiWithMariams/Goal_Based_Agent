
# 🎯 Goal-Based Job Application Assistant (LangChain + Groq + Streamlit)

This project demonstrates a **Goal-Based AI Agent** built using **LangChain and Groq LLM**, integrated with a **Streamlit web interface**.

The agent interacts with the user to collect required job application details and ensures all information is complete before submission.

---

## 📌 Project Concept

This project is based on the **Goal-Based Agent model** from Artificial Intelligence.

### 🧠 Agent Goal:

Collect the following required information:

* Name
* Email
* Skills

### 🤖 Agent Behavior:

* Extracts information from user chat
* Optionally extracts data from uploaded resume (PDF)
* Checks whether all required fields are completed
* Stops once the goal is achieved
* Allows downloading a summary file

Unlike a reflex agent, this agent:

* Maintains memory (ConversationBufferMemory)
* Tracks goal completion
* Makes decisions based on collected data

---

## 🗂️ Application Flow

1. User provides details via chat
2. OR uploads a resume (PDF)
3. System extracts:

   * Name
   * Email
   * Skills
4. Agent checks completion status
5. When complete:

   * Displays success message
   * Enables download option

---

## ⚙️ Technologies Used

* Python 3.10+
* Streamlit (Frontend UI)
* LangChain (Agent framework)
* Groq LLM (llama-3.1-8b-instant)
* PyMuPDF (PDF text extraction)
* Regex (Information parsing)

---

## 📁 Files

```
goal_based_agent_with_streamlitfrontend.py  → Main application
requirements.txt                             → Dependencies
README.md                                     → Documentation
.env                                          → API key file
```

---

## 📦 Installation

### 1️⃣ Install Required Libraries

```
pip install -r requirements.txt
```

requirements.txt:

```
langchain==0.2.16
langchain-groq==0.1.5
python-dotenv==1.0.1
streamlit==1.37.1
pymupdf==1.24.9
```

---

## 🔑 Environment Setup

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:
[https://console.groq.com/](https://console.groq.com/)

---

## ▶️ How to Run the Project

```
streamlit run goal_based_agent_with_streamlitfrontend.py
```

A browser window will open showing the interactive chat interface.

---

## 🧠 Key Components Explained

### extract_application_info(text)

* Extracts name, email, and skills from user chat
* Uses flexible regex patterns

### extract_info_from_cv(text)

* Extracts information from uploaded resume
* Detects first-line name
* Extracts email using regex
* Finds skills section

### check_application_goal()

* Checks whether all required fields are filled
* Returns missing fields if incomplete
* Confirms readiness when complete

---

## 📊 Application Output

* Real-time chat interface
* Goal completion tracking
* Status messages
* Downloadable application summary (.txt)
* Reset chat functionality

---

## 🎯 Learning Outcomes

* Understanding Goal-Based Agents
* Building LLM-powered AI systems
* Integrating LangChain with Groq
* Streamlit UI state management
* PDF text extraction
* Regex-based information parsing

---

## 🚀 Future Improvements

* AI-based structured resume extraction (LLM JSON output)
* Multi-user support with database
* Form validation system
* Deployment on Streamlit Cloud
* Add evaluation metrics
* Convert to Model-Based Agent

---

## 👩‍💻 Author

MaryamS
GenAI Developer | AI | Machine Learning | NLP

---

✅ Application Complete — Goal-Based Agent successfully collects required information!

