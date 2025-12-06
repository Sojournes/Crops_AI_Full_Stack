from fastapi import APIRouter, HTTPException
from ..model_schemas import ChatRequest, ChatResponse
from ..genai_service import GenAIService

router = APIRouter()
genai_service = None

@router.on_event("startup")
async def startup_event():
    global genai_service
    try:
        genai_service = GenAIService()
    except Exception as e:
        print(f"Failed to initialize GenAI Service: {e}")

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not genai_service:
        raise HTTPException(status_code=500, detail="GenAI Service not initialized. Check API Key.")
    
    response_text, updated_history = genai_service.get_chat_response(request.message, request.history)
    return ChatResponse(response=response_text, history=updated_history)
