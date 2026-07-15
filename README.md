# 🧞 EduGenie Google Gemini Powered Learning Assistant

An AI-powered learning assistant that helps students understand complex topics, generate quizzes, and personalize their study plans using Google Gemini AI.

Built using **Web Technologies (React/Next.js)**, **Node.js/Python Backend**, and the **Google Gemini API**.

---

## 📌 Features

- 🔍 Analyze learning materials and documents
- 🧠 Generate personalized study guides using Gemini AI
- 💬 Interactive chat for tutoring and Q&A
- 📚 Topic summarization and explanation
- 📝 Auto-generate quizzes to test knowledge
- 👍👎 Collect user feedback on learning progress

---

## 🏗️ Project Architecture

```text
User
  ↓
Frontend Web Application
  ↓
Backend API Server
  ↓
Services Layer
 ├── Content Analyzer
 ├── Chat/Tutor Engine
 ├── Quiz Generator
 └── Progress Tracker
  ↓
Database + Google Gemini API
```

---

## 📂 Project Structure

```text
edugenie-learning-assistant/
│
├── backend/
│   ├── main.py (or index.js)
│   ├── routes/
│   └── services/
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── docs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features.md
│   ├── setup.md
│   └── technologies.md
│
├── README.md
└── .env
```

---

## ⚙️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Next.js / React | Frontend UI |
| Node.js / Python | Backend API |
| Google Gemini API | Core AI & NLP Processing |
| MongoDB / PostgreSQL | Database Storage |
| Git & GitHub | Version Control |
