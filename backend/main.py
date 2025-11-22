"""
FastAPI Application for Multi-Agent Tourism System
Demonstrates full-stack AI agent development with proper API design.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional
import os
from dotenv import load_dotenv

from agents import parent_agent
from utils import format_error_response, logger

# Import settings
try:
    from settings import settings
    RATE_LIMIT_REQUESTS = settings.rate_limit_requests
    RATE_LIMIT_WINDOW = settings.rate_limit_window
except ImportError:
    RATE_LIMIT_REQUESTS = 10
    RATE_LIMIT_WINDOW = 60

import time
from collections import defaultdict, Counter
from datetime import datetime

# Load environment variables
load_dotenv()

# Application metrics
app_start_time = datetime.now()
request_count = 0
search_stats = Counter()

# Rate limiting storage
rate_limit_storage = defaultdict(list)

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
    
    @validator('location')
    def validate_location(cls, v):
        """Validate location input."""
        if not v or not v.strip():
            raise ValueError('Location cannot be empty')
        if len(v) > 100:
            raise ValueError('Location name too long (max 100 characters)')
        # Basic XSS prevention
        if '<' in v or '>' in v:
            raise ValueError('Invalid characters in location')
        return v.strip()
    
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


@app.get("/api/stats")
async def get_stats():
    """
    Get application statistics and performance metrics.
    Demonstrates monitoring and analytics capabilities.
    """
    uptime_seconds = (datetime.now() - app_start_time).total_seconds()
    
    return {
        "status": "operational",
        "uptime_seconds": uptime_seconds,
        "uptime_human": f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m",
        "total_requests": request_count,
        "top_searches": dict(search_stats.most_common(10)),
        "cache_info": "enabled",
        "rate_limit": f"{RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW}s"
    }


@app.post("/api/plan-trip", response_model=TripPlanResponse)
async def plan_trip(request: TripPlanRequest, http_request: Request):
    """
    Main endpoint for trip planning.
    
    This endpoint demonstrates:
    - Taking responsibility of the AI agent as a whole
    - Processing user requests through multi-agent system
    - Proper error handling and debugging
    - Request validation and rate limiting
    
    Args:
        request: Trip planning request with location
        http_request: FastAPI request object for rate limiting
        
    Returns:
        Trip planning response with weather and/or places information
    """
    global request_count
    
    # Rate limiting
    client_ip = http_request.client.host
    current_time = time.time()
    
    # Clean old entries
    rate_limit_storage[client_ip] = [
        t for t in rate_limit_storage[client_ip] 
        if current_time - t < RATE_LIMIT_WINDOW
    ]
    
    # Check rate limit
    if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_REQUESTS:
        logger.warning(f"Rate limit exceeded for {client_ip}")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )
    
    # Record request
    rate_limit_storage[client_ip].append(current_time)
    request_count += 1
    search_stats[request.location.lower()] += 1
    
    try:
        logger.info(f"Received trip planning request for: {request.location}")
        
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
