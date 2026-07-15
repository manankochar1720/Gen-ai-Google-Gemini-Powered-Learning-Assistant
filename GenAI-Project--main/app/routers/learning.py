from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import (
    ExplainRequest, ExplainResponse,
    ChatRequest, ChatResponse,
    QuizRequest, QuizResponse,
    QuizScoreRequest, QuizScoreResponse, QuizQuestionResult,
    FeedbackRequest
)
from app.services import gemini_service
from app.services import history_logger
from app.services import feedback_logger
from app.services import pdf_generator
import datetime

router = APIRouter(prefix="/api")

@router.post("/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest):
    try:
        explanation_data = gemini_service.explain_topic(
            topic=request.topic,
            level=request.level,
            style=request.style
        )
        
        # Add timestamp and log to history
        session_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "explanation",
            "request": request.model_dump(),
            "response": explanation_data
        }
        history_logger.save_history(session_log)
        
        return explanation_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
def chat_tutor(request: ChatRequest):
    try:
        reply = gemini_service.chat_tutor(
            topic=request.topic,
            query=request.query,
            history=[m.model_dump() for m in request.history]
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quiz/generate", response_model=QuizResponse)
def generate_quiz(request: QuizRequest):
    try:
        quiz_data = gemini_service.generate_quiz(
            topic=request.topic,
            num_questions=request.num_questions,
            level=request.level
        )
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quiz/evaluate", response_model=QuizScoreResponse)
def evaluate_quiz(request: QuizScoreRequest):
    try:
        results = []
        score = 0
        total = len(request.questions)
        
        for idx, q in enumerate(request.questions):
            user_idx = request.user_answers[idx] if idx < len(request.user_answers) else -1
            is_correct = (user_idx == q.correct_index)
            if is_correct:
                score += 1
                
            results.append(
                QuizQuestionResult(
                    question=q.question,
                    options=q.options,
                    correct_index=q.correct_index,
                    user_index=user_idx,
                    is_correct=is_correct,
                    explanation=q.explanation
                )
            )
            
        percentage = (score / total * 100) if total > 0 else 0.0
        
        # Simple rule-based feedback
        if percentage == 100:
            feedback = "Outstanding! Perfect score. You have fully mastered this topic."
        elif percentage >= 70:
            feedback = "Great job! You have a solid grasp. Review the incorrect answers to refine your understanding."
        elif percentage >= 40:
            feedback = "Good effort! Try reading the explanation again and retaking the quiz to improve your score."
        else:
            feedback = "Keep learning! Don't worry, review the topic details, ask the AI Tutor questions, and try again."
            
        # Log quiz results to history
        session_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "quiz",
            "topic": request.topic,
            "score": score,
            "total": total,
            "percentage": percentage,
            "feedback": feedback
        }
        history_logger.save_history(session_log)
        
        return {
            "score": score,
            "total": total,
            "percentage": percentage,
            "feedback": feedback,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    try:
        feedback_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "rating": request.rating,
            "suggestion": request.suggestion
        }
        feedback_logger.save_feedback(feedback_data)
        return {"message": "Feedback submitted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_history():
    try:
        return history_logger.get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pdf/explanation")
def download_explanation_pdf(data: dict):
    try:
        # data should have topic, level, style, explanation, analogies, key_highlights, study_plan
        pdf_buffer = pdf_generator.generate_explanation_pdf(data)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=explanation_{data.get('topic','topic')}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pdf/quiz")
def download_quiz_pdf(data: dict):
    try:
        # data should have topic, questions: [question, options, correct_index, explanation]
        pdf_buffer = pdf_generator.generate_quiz_pdf(data)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=quiz.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
