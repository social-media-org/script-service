#!/usr/bin/env python3
"""Run script for Script Generation Service that fixes import path issues."""

import sys
import os

print("Current working directory:", os.getcwd())
print("Script directory:", os.path.dirname(os.path.abspath(__file__)))

# Add current directory to Python path first
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Remove any paths that contain ui-service to avoid conflicts
sys.path = [p for p in sys.path if 'ui-service' not in p]

print("Python path after filtering:")
for p in sys.path:
    print("  ", p)

# Now import the app
try:
    from app.main import app
    print("Successfully imported app from script-service")
except ImportError as e:
    print(f"Import error: {e}")
    raise

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8002
    port = int(os.getenv("PORT", 8002))
    
    print(f"Starting Script Generation Service on port {port}")
    print(f"Python path: {sys.path}")
    
    # Use import string for reload to work
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
        reload_dirs=[os.path.dirname(os.path.abspath(__file__))]
    )
