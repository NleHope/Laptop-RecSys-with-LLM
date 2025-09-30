from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables
from models import ChatMessage, ChatResponse, SlotMemory
from services import ProductService, SessionService
from llm_service import llm_service
from demo_llm_service import demo_llm_service
import uuid
import os
from typing import Dict, Any

app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """Main chat endpoint that handles conversation flow"""
    try:
        # Initialize services
        session_service = SessionService(db)
        product_service = ProductService(db)
        
        # Choose LLM service based on Google API key availability
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key and google_api_key != "your_google_api_key_here":
            print(f"Using Google Gemini API with key: {google_api_key[:5]}...")
            current_llm_service = llm_service
        else:
            print("No valid Google API key found. Using demo LLM service.")
            current_llm_service = demo_llm_service
        
        # Get or create session memory
        current_memory = session_service.get_or_create_session(message.session_id)
        
        # Extract information from user message
        updated_memory = current_llm_service.extract_information(message.message, current_memory)
        
        # Update session in database
        session_service.update_session(message.session_id, updated_memory)
        
        # Check if we should recommend products
        should_recommend = session_service.should_recommend_products(updated_memory)
        
        recommended_products = []
        if should_recommend:
            # Search for products
            products = product_service.search_products(updated_memory)
            recommended_products = [product.dict() for product in products]
            
            # Generate response with product recommendations
            reply = current_llm_service.generate_response(
                message.message, 
                updated_memory, 
                recommended_products
            )
            
            return ChatResponse(
                reply=reply,
                session_id=message.session_id,
                needs_more_info=False,
                recommended_products=recommended_products
            )
        else:
            # Generate response asking for more information
            reply = current_llm_service.generate_response(message.message, updated_memory)
            
            return ChatResponse(
                reply=reply,
                session_id=message.session_id,
                needs_more_info=True,
                recommended_products=[]
            )
            
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return ChatResponse(
            reply="I apologize, but I'm having some technical difficulties. Please try again.",
            session_id=message.session_id,
            needs_more_info=True,
            recommended_products=[]
        )

@app.get("/session/{session_id}/memory")
async def get_session_memory(session_id: str, db: Session = Depends(get_db)):
    """Get current memory state for a session (for debugging)"""
    session_service = SessionService(db)
    memory = session_service.get_or_create_session(session_id)
    return memory.dict()

@app.post("/session/new")
async def create_new_session():
    """Create a new session ID"""
    return {"session_id": str(uuid.uuid4())}

@app.get("/products/search")
async def search_products_endpoint(
    budget: float = None,
    category: str = None,
    purpose: str = None,
    db: Session = Depends(get_db)
):
    """Direct product search endpoint (for testing)"""
    memory = SlotMemory(
        budget=budget,
        category=category,
        purpose=purpose
    )
    
    product_service = ProductService(db)
    products = product_service.search_products(memory)
    
    return [product.dict() for product in products]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
