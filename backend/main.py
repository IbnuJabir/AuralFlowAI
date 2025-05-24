# backend/main.py - Add these imports and router inclusion
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import your existing routers
from app.api.routes import auth, users, videos, voice

# Create FastAPI app
app = FastAPI(
    title="Voice Dubbing & Cloning API",
    description="API for voice dubbing and cloning in multiple languages",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(auth.router, prefix="/api")
# app.include_router(users.router, prefix="/api")
# app.include_router(videos.router, prefix="/api")
app.include_router(voice.router, prefix="/api")  # Add the voice router

# Serve uploaded files (optional - for serving processed audio files)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    return {"message": "Voice Dubbing & Cloning API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "voice-dubbing-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# backend/requirements.txt additions - Add these to your pyproject.toml or requirements.txt
"""
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
celery[redis]>=5.3.0
redis>=5.0.0
python-multipart>=0.0.6
requests>=2.31.0
python-magic>=0.4.27
pydantic>=2.5.0
"""