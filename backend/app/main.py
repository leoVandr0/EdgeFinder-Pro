from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.routers import strength, insights, events, pair_compare, news_summary

# Create FastAPI app
app = FastAPI(
    title="EdgeFinder Pro API",
    description="Advanced forex analytics and trading insights platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(strength.router)
app.include_router(insights.router)
app.include_router(events.router)
app.include_router(pair_compare.router)
app.include_router(news_summary.router)

# Health check endpoint
@app.get("/")
async def root():
    """API health check and information"""
    return {
        "service": "EdgeFinder Pro API",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "strength": "/api/strength",
            "insights": "/api/insights",
            "events": "/api/events",
            "pair_compare": "/api/pair-compare",
            "news_summary": "/api/news-summary"
        }
    }

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("Starting EdgeFinder Pro API...")
    print(f"CORS enabled for: {allowed_origins}")

    # Initialize databases (if configured)
    try:
        from app.services.db import connect_mongodb, init_postgres
        # MongoDB connection (optional)
        if os.getenv("MONGODB_URI"):
            await connect_mongodb()
        # PostgreSQL connection (optional)
        if os.getenv("POSTGRES_URL"):
            await init_postgres()
    except Exception as e:
        print(f"Database initialization warning: {e}")
        print("Running with in-memory fallback")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down EdgeFinder Pro API...")
    try:
        from app.services.db import close_mongodb
        await close_mongodb()
    except Exception as e:
        print(f"Shutdown cleanup warning: {e}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("ENVIRONMENT") == "development" else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
