#!/usr/bin/env python3
"""
UpShiftRx API Server Launcher
Run: python start_api.py
"""

import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    print("🚀 Starting UpShiftRx API Server...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )