from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from .routes.lottery_routes import router as lottery_router
from .models.lottery import APIResponse

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Lottery Checker API",
    description="Multi-country lottery number checking and historical data API. Check lottery numbers against historical draws and get prize information.",
    version="1.0.0",
    contact={
        "name": "Lottery Checker API Support",
        "url": "http://localhost:8000",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    servers=[
        {
            "url": os.getenv("API_URL", "https://lottery-checker-api-lime.vercel.app"),
            "description": "Production server"
        },
        {
            "url": os.getenv("DEV_API_URL", "http://localhost:8000"),
            "description": "Development server"
        }
    ],
    tags_metadata=[
        {
            "name": "Thailand Lottery",
            "description": "Thai lottery operations",
        },
        {
            "name": "system",
            "description": "System endpoints",
        },
    ]
)

# Add CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(lottery_router, prefix="/api")

@app.get("/", response_model=APIResponse, tags=["system"])
async def root():
    """Get API information and available endpoints."""
    return APIResponse(
        success=True,
        message="Lottery Checker API is running",
        data={
            "api_info": {
                "title": "Lottery Checker API",
                "version": "1.0.0",
                "description": "Multi-country lottery number checking API",
                "status": "Operational"
            },
            "documentation": {
                "swagger_ui": "/docs",
                "redoc": "/redoc",
                "markdown_docs": "See API_DOCUMENTATION.md file"
            },
            "endpoints": {
                "check_lottery_numbers": {
                    "url": "/api/th/v1/lottery/check",
                    "method": "POST",
                    "description": "Check your lottery numbers for winnings"
                },
                "latest_draw": {
                    "url": "/api/th/v1/lottery/draws/latest", 
                    "method": "GET",
                    "description": "Get the most recent lottery draw"
                },
                "all_draws": {
                    "url": "/api/th/v1/lottery/draws",
                    "method": "GET", 
                    "description": "Get all lottery draws (paginated)"
                },
                "draw_by_date": {
                    "url": "/api/th/v1/lottery/draws/{date}",
                    "method": "GET",
                    "description": "Get lottery draw for specific date"
                },
                "search_draws": {
                    "url": "/api/th/v1/lottery/search",
                    "method": "GET",
                    "description": "Search draws with date filters"
                }
            },
            "database_stats": {
                "total_draws": 429,
                "date_range": "2022-12-16 to 2024-12-16",
                "latest_draw": "2024-12-16"
            },
            "prize_structure": {
                "1st_prize": "฿6,000,000",
                "around_1st": "฿100,000",
                "2nd_prize": "฿200,000",
                "3rd_prize": "฿80,000",
                "4th_prize": "฿40,000", 
                "5th_prize": "฿20,000",
                "3_digits": "฿4,000",
                "2_digits": "฿2,000"
            }
        }
    )

@app.get("/health", response_model=APIResponse, tags=["system"])
async def health_check():
    """Check API health and database connectivity."""
    from datetime import datetime
    import time
    
    start_time = time.time()
    
    # Test database connectivity
    try:
        from app.core.database import get_supabase_client
        client = get_supabase_client()
        # Simple query to test connection
        client.table("lottery_draws").select("*").limit(1).execute()
        db_status = "Connected"
        db_healthy = True
    except Exception as e:
        db_status = f"Error: {str(e)[:50]}..."
        db_healthy = False
    
    response_time = round((time.time() - start_time) * 1000, 2)
    
    return APIResponse(
        success=True,
        message="Health check completed",
        data={
            "status": "Healthy" if db_healthy else "Degraded",
            "timestamp": datetime.now().isoformat(),
            "database": {
                "status": db_status,
                "healthy": db_healthy
            },
            "performance": {
                "response_time_ms": response_time,
                "status": "Fast" if response_time < 1000 else "Slow"
            },
            "api": {
                "version": "1.0.0",
                "uptime": "Running"
            }
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc),
            "data": None
        }
    )

# HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error": f"HTTP {exc.status_code}",
            "data": None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 