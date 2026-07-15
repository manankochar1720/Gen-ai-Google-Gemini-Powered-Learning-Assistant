from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.learning import router as learning_router

app = FastAPI(
    title="EduGenie Google Gemini Powered Learning Assistant",
    description="Backend API for explaining topics, tutoring, quiz generation, and progress tracking.",
    version="1.0.0"
)

# Enable CORS for frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits access from local dev clients or Streamlit
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the learning API routes
app.include_router(learning_router)

from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    prompt: Optional[str] = None
    tone: Optional[str] = None
    platform: Optional[str] = None

@app.post("/generate")
def generate_captions(request: GenerateRequest):
    return {
        "captions": [
            "Sunshine vibes and good times ☀️ #SummerFeels",
            "Sustainable style for a brighter tomorrow 🌱",
            "Look good, feel good, do good 💚"
        ],
        "hashtags": [
            "#sunglasses", "#sustainablefashion", "#summerstyle", "#ecofriendly",
            "#sustainability", "#fashion", "#styleinspo", "#summervibes", "#greencollection", "#wearsustainable"
        ],
        "ctas": [
            "Shop the collection now!",
            "Grab yours before it's gone!",
            "Make a sustainable choice today!"
        ]
    }

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "EduGenie Learning Assistant API Running",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    from app.config import HOST, PORT
    print(f"Starting server on {HOST}:{PORT}")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
