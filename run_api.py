#!/usr/bin/env python3
"""
Script to run the Lottery Checker API server
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the FastAPI server"""
    print("🎲 Starting Lottery Checker API...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000/api/v1")
    print("="*60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 