"""
FastAPI Application for Multi-Agent Tourism System
Demonstrates full-stack AI agent development with proper API design.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from agents import parent_agent
from utils import format_error_response, logger

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Tourism System",
    description="AI-powered tourism planning with multi-agent orchestration",
    version="1.0.0"
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5500")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://127.0.0.1:5500", "*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class TripPlanRequest(BaseModel):
    """Request model for trip planning."""
    location: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Bangalore"
            }
        }


class TripPlanResponse(BaseModel):
    """Response model for trip planning."""
    success: bool
    response: str
    query_type: Optional[str] = None
    location: Optional[str] = None
    weather: Optional[dict] = None
    places: Optional[dict] = None


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Multi-Agent Tourism System",
        "version": "1.0.0",
        "description": "AI-powered tourism planning using LangGraph multi-agent orchestration",
        "endpoints": {
            "plan_trip": "/api/plan-trip",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Multi-Agent Tourism System"
    }


@app.post("/api/plan-trip", response_model=TripPlanResponse)
async def plan_trip(request: TripPlanRequest):
    """
    Main endpoint for trip planning.
    
    This endpoint demonstrates:
    - Taking responsibility of the AI agent as a whole
    - Processing user requests through multi-agent system
    - Proper error handling and debugging
    
    Args:
        request: Trip planning request with location
        
    Returns:
        Trip planning response with weather and/or places information
    """
    try:
        logger.info(f"Received trip planning request for: {request.location}")
        
        # Validate input
        if not request.location or not request.location.strip():
            raise HTTPException(
                status_code=400,
                detail="Location cannot be empty"
            )
        
        # Process through parent agent
        result = await parent_agent.process_query(request.location.strip())
        
        logger.info(f"Successfully processed request for: {request.location}")
        
        return TripPlanResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing trip request: {str(e)}", exc_info=True)
        error_response = format_error_response(e)
        
        return TripPlanResponse(
            success=False,
            response=error_response["message"],
            location=request.location
        )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Multi-Agent Tourism System starting up...")
    logger.info(f"Frontend URL: {frontend_url}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Multi-Agent Tourism System shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
