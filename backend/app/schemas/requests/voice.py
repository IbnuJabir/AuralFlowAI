# backend/app/schemas/requests/voice.py
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Literal
from fastapi import UploadFile

class VoiceCloneRequest(BaseModel):
    type: Literal["file", "link"]
    source: Optional[str] = "unknown"
    target_language: Optional[str] = "en"  # Language to clone voice into
    voice_settings: Optional[dict] = None  # Additional voice cloning parameters
