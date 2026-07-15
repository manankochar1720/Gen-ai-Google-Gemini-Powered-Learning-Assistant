import json
import logging
import requests
from app.config import GEMINI_API_KEY

# Configure logger
logger = logging.getLogger("EduGenie.GeminiService")
logging.basicConfig(level=logging.INFO)

# Validate API availability
api_available = True if GEMINI_API_KEY else False
if api_available:
    logger.info("Google Gemini REST API configured successfully.")
else:
    logger.warning("GEMINI_API_KEY not found in environment. Running in Mock fallback mode.")

# Base URL for Google Gemini REST API (using gemini-2.5-flash which is widely supported and fast)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def clean_gemini_json(data):
    """
    Recursively scans and replaces raw unescaped '\\n' string structures
    back into real control character newlines so they render correctly in markdown.
    """
    if isinstance(data, str):
        return data.replace("\\n", "\n").replace(r"\n", "\n")
    elif isinstance(data, list):
        return [clean_gemini_json(item) for item in data]
    elif isinstance(data, dict):
        return {k: clean_gemini_json(v) for k, v in data.items()}
    return data

def explain_topic(topic: str, level: str, style: str) -> dict:
    """
    Generates a structured explanation for a topic using Gemini REST API,
    customized by the student's level and learning style.
    """
    if not api_available:
        return get_mock_explanation(topic, level, style)

    prompt = f"""
    You are EduGenie, a world-class personalized tutor. Explain the topic: "{topic}".
    
    Target Audience Profile:
    - Knowledge Level: {level} (Beginner: simple concepts, no jargon; Intermediate: deeper detail, definitions; Advanced: complex trade-offs, architecture, technical details)
    - Learning Style: {style} (Visual: detailed analogies, ASCII flowcharts, markdown tables; Verbal: engaging text, conceptual metaphors; Practical: code snippets, hands-on tasks; Intuitive: high-level thought experiments, core 'why' questions)
    
    Instruction details:
    1. Format structured tables to illustrate flows, comparisons, and attributes.
    2. Include clickable markdown links (e.g., [Official Docs](https://example.com)) to official resources or reference links if they are highly relevant and important for the topic.
    3. Generate a clean Mermaid.js diagram representing the concept's workflow, architecture, or structure. The diagram code must start with "graph TD" or "graph LR" on its own line. Each node link statement must be on a new line (using \n) or separated by a semicolon (;), for example: "graph TD\n  A[Client] --> B[API]\n  B --> C[Server]". Node labels must be simple, concise alphanumeric text and must NOT contain parentheses, slashes (/), or special characters. Do not wrap the code in backticks.
    4. Output the details matching the GeminiExplainSchema structure.
    """

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "topic": {"type": "STRING"},
                    "level": {"type": "STRING"},
                    "style": {"type": "STRING"},
                    "explanation": {"type": "STRING"},
                    "analogies": {"type": "STRING"},
                    "mermaid_diagram": {"type": "STRING"},
                    "key_highlights": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "study_plan": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                },
                "required": ["topic", "level", "style", "explanation", "analogies", "mermaid_diagram", "key_highlights", "study_plan"]
            }
        }
    }

    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"Gemini API returned error {response.status_code}: {response.text}")
            raise Exception(f"API Error {response.status_code}")
            
        res_json = response.json()
        text_content = res_json["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(text_content)
        return clean_gemini_json(data)
        
    except Exception as e:
        logger.error(f"Error calling Gemini REST explain_topic: {e}. Falling back to mock data.")
        return get_mock_explanation(topic, level, style)

def chat_tutor(topic: str, query: str, history: list) -> str:
    """
    Conducts a tutoring conversation about the topic, preserving history.
    """
    if not api_available:
        return f"Mock Tutor Response: That is a great question about {topic}! In a live environment with your Gemini API key, I would analyze your question '{query}' and provide a personalized response."

    # Build prompt contents with history
    contents = []
    for m in history:
        # Gemini API role must be 'user' or 'model' (not 'assistant')
        role = "user" if m["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": m["content"]}]
        })
        
    system_instruction = f"""
    You are EduGenie, an AI tutor. The student is currently studying: "{topic}".
    Be encouraging, detailed, clear, and direct. Guide them to understand rather than just giving the answers when appropriate.
    Keep the explanation educational.
    """

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        }
    }

    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, json=payload, timeout=20)
        
        if response.status_code != 200:
            logger.error(f"Gemini Chat API returned error {response.status_code}: {response.text}")
            raise Exception(f"API Error {response.status_code}")
            
        res_json = response.json()
        reply_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
        return clean_gemini_json(reply_text) if isinstance(reply_text, str) else reply_text
        
    except Exception as e:
        logger.error(f"Error in Gemini REST chat_tutor: {e}")
        return f"I'm sorry, I encountered an error connecting to my learning engine. Let's try again. (Detail: {e})"

def generate_quiz(topic: str, num_questions: int, level: str) -> dict:
    """
    Generates a multiple choice quiz on the topic.
    """
    if not api_available:
        return get_mock_quiz(topic, num_questions, level)

    import time
    import random

    prompt = f"""
    Create a multiple choice quiz about the topic "{topic}" for a student at the "{level}" level.
    The quiz should contain exactly {num_questions} questions.
    
    Ensure that the questions generated are unique, creative, and test different aspects of "{topic}".
    Seed identifier: {time.time()} (use this seed to generate distinct question variations).
    """

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "topic": {"type": "STRING"},
                    "questions": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "question": {"type": "STRING"},
                                "options": {
                                    "type": "ARRAY",
                                    "items": {"type": "STRING"}
                                },
                                "correct_index": {"type": "INTEGER"},
                                "explanation": {"type": "STRING"}
                              },
                              "required": ["question", "options", "correct_index", "explanation"]
                        }
                    }
                },
                "required": ["topic", "questions"]
            }
        }
    }

    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"Gemini Quiz API returned error {response.status_code}: {response.text}")
            raise Exception(f"API Error {response.status_code}")
            
        res_json = response.json()
        text_content = res_json["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(text_content)
        return clean_gemini_json(data)
        
    except Exception as e:
        logger.error(f"Error calling Gemini REST generate_quiz: {e}. Falling back to mock quiz.")
        return get_mock_quiz(topic, num_questions, level)


# ---------------------------------------------------------------------------
# Mock Fallbacks (for out-of-the-box operation without API keys)
# ---------------------------------------------------------------------------

def get_mock_explanation(topic: str, level: str, style: str) -> dict:
    return {
        "topic": topic,
        "level": level,
        "style": style,
        "explanation": f"""### Understanding {topic} ({level} Level)
*Note: This is a high-quality local demonstration explanation since the Google Gemini API key is not currently configured.*

{topic} is a fundamental concept. At a **{level}** level, we analyze how its components interact. 

1. **Core Concept**: It operates by defining rules that simplify complex structures.
2. **Key Mechanisms**:
   - Component isolation and abstraction.
   - Flow modeling and state management.
   - Interactive feedback loops.

#### Further Exploration
For a **{style}** learner, the best way to understand this is to break down the structure and experiment with the parameters directly.""",
        "analogies": f"Think of {topic} like a **post office system**. Just as letters are labeled, routed, and delivered through standard layers, {topic} manages information flow by encapsulating details and forwarding results.",
        "mermaid_diagram": "graph TD;\n    A[Post Office] -->|routes| B[Letters];\n    B -->|delivers| C[Recipient];",
        "key_highlights": [
            f"Encapsulation: Isolating details in {topic}",
            "Routing: Moving information between states",
            "Feedback: Validating outcomes automatically"
        ],
        "study_plan": [
            f"Step 1: Read the introductory documentation for {topic}.",
            f"Step 2: Complete the hands-on code template for {topic} in python.",
            f"Step 3: Analyze performance constraints and edge cases."
        ]
    }

def get_mock_quiz(topic: str, num_questions: int, level: str) -> dict:
    import random
    pool = [
        {
            "question": f"Which of the following best describes the core mechanism of {topic}?",
            "options": [
                "Layered abstraction and modular separation.",
                "Sequential processing without feedback loops.",
                "Monolithic execution templates with single entry points.",
                "Manual human validation at every execution state."
            ],
            "correct_index": 0,
            "explanation": "Abstraction isolates internal details, simplifying external communication."
        },
        {
            "question": f"What is a primary advantage of applying {topic} in modern systems design?",
            "options": [
                "Scalability, low maintenance overhead, and ease of unit testing.",
                "Higher memory consumption and latency overhead.",
                "Complete removal of compilers and execution runtimes.",
                "Locking of CPU cycles to obsolete platforms."
            ],
            "correct_index": 0,
            "explanation": "Abstraction permits components to scale and be tested in modular isolation."
        },
        {
            "question": f"When would a developer avoid implementing {topic} models?",
            "options": [
                "In tight, low-resource embedded environments where compiler overhead is critical.",
                "When building enterprise level web clients.",
                "When developing code within a multi-member team.",
                "When accuracy and speed are key properties of the system."
            ],
            "correct_index": 0,
            "explanation": "In deeply restricted embedded microchips, any minor abstraction overhead might exceed memory limits."
        },
        {
            "question": f"Which component represents the primary performance bottleneck in {topic} pipelines?",
            "options": [
                "State synchronization across distributed boundaries.",
                "Reading static configuration comments from text files.",
                "Drawing visual flowchart layouts on screens.",
                "Setting local environment variables."
            ],
            "correct_index": 0,
            "explanation": "Sharing state variables dynamically across distinct network systems takes high latency."
        },
        {
            "question": f"How does the difficulty level '{level}' typically affect a {topic} study track?",
            "options": [
                "It guides the level of depth, math background, and coding complexity included.",
                "It has no structural effect on explanations.",
                "It forces hardware units to decrease execution speed.",
                "It restricts developers from deploying guides offline."
            ],
            "correct_index": 0,
            "explanation": "Difficulty categories structure how deep the underlying mechanics are researched."
        }
    ]
    random.shuffle(pool)
    questions = []
    for i in range(num_questions):
        q = pool[i % len(pool)]
        questions.append({
            "question": q["question"],
            "options": q["options"],
            "correct_index": q["correct_index"],
            "explanation": q["explanation"]
        })
    return {
        "topic": topic,
        "questions": questions
    }
