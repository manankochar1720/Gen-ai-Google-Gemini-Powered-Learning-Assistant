import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import json

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "service" in data

def test_explain_endpoint():
    payload = {
        "topic": "Neural Networks",
        "level": "Beginner",
        "style": "Visual"
    }
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Neural Networks"
    assert "explanation" in data
    assert "analogies" in data
    assert "key_highlights" in data
    assert "study_plan" in data

def test_chat_endpoint():
    payload = {
        "topic": "Neural Networks",
        "query": "How many layers do they have?",
        "history": [
            {"role": "assistant", "content": "Hi, I am your tutor."},
            {"role": "user", "content": "I want to learn about Neural Networks."}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data

def test_quiz_generate_endpoint():
    payload = {
        "topic": "React Hooks",
        "num_questions": 2,
        "level": "Beginner"
    }
    response = client.post("/api/quiz/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "React Hooks"
    assert len(data["questions"]) > 0
    assert "options" in data["questions"][0]

def test_quiz_evaluate_endpoint():
    payload = {
        "topic": "React Hooks",
        "questions": [
            {
                "question": "What hook manages state?",
                "options": ["useState", "useEffect", "useContext", "useReducer"],
                "correct_index": 0,
                "explanation": "useState manages state."
            }
        ],
        "user_answers": [0]
    }
    response = client.post("/api/quiz/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 1
    assert data["total"] == 1
    assert data["percentage"] == 100.0
    assert len(data["results"]) == 1
    assert data["results"][0]["is_correct"] is True

def test_feedback_endpoint():
    payload = {
        "rating": 5,
        "suggestion": "Great tool! Love the explanation models."
    }
    response = client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Feedback submitted successfully" in data["message"]

def test_history_endpoint():
    response = client.get("/api/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_pdf_explanation_endpoint():
    payload = {
        "topic": "Quantum Theory",
        "level": "Advanced",
        "style": "Intuitive",
        "explanation": "Deep explanations of quantum mechanics.",
        "analogies": "It is like a coin spinning on a table.",
        "key_highlights": ["Superposition", "Entanglement"],
        "study_plan": ["Step 1", "Step 2"]
    }
    response = client.post("/api/pdf/explanation", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_pdf_quiz_endpoint():
    payload = {
        "topic": "Quantum Theory",
        "questions": [
            {
                "question": "What is superposition?",
                "options": ["A state of both 0 and 1", "Only 0", "Only 1", "None"],
                "correct_index": 0,
                "explanation": "Superposition represents multiple states simultaneously."
            }
        ]
    }
    response = client.post("/api/pdf/quiz", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
