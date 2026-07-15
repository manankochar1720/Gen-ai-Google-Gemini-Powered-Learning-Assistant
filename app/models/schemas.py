from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExplainRequest(BaseModel):
    topic: str = Field(..., description="The subject or topic to explain")
    level: str = Field("Beginner", description="Learning level: Beginner, Intermediate, or Advanced")
    style: str = Field("Visual", description="Learning style preference: Visual, Verbal, Practical, or Intuitive")

class ExplainResponse(BaseModel):
    topic: str
    level: str
    style: str
    explanation: str
    analogies: str
    mermaid_diagram: str
    key_highlights: List[str]
    study_plan: List[str]

class ChatMessage(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    topic: str = Field(..., description="Topic of the current learning session")
    query: str = Field(..., description="User follow-up question")
    history: List[ChatMessage] = Field(default=[], description="Chat transcript history")

class ChatResponse(BaseModel):
    reply: str

class QuizRequest(BaseModel):
    topic: str = Field(..., description="The topic for the quiz")
    num_questions: int = Field(3, description="Number of questions to generate")
    level: str = Field("Beginner", description="Learning level")

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    explanation: str

class QuizResponse(BaseModel):
    topic: str
    questions: List[QuizQuestion]

class QuizScoreRequest(BaseModel):
    topic: str
    questions: List[QuizQuestion]
    user_answers: List[int] = Field(..., description="Indices of options chosen by user")

class QuizQuestionResult(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    user_index: int
    is_correct: bool
    explanation: str

class QuizScoreResponse(BaseModel):
    score: int
    total: int
    percentage: float
    feedback: str
    results: List[QuizQuestionResult]

class FeedbackRequest(BaseModel):
    rating: int = Field(..., description="Rating score from 1 to 5")
    suggestion: str = Field(..., description="Written feedback or suggestions")
