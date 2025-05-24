
# backend/app/schemas/responses/voice.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class VoiceCloneResponse(BaseModel):
    success: bool
    message: str
    task_id: Optional[str] = None
    status: str = "submitted"  # submitted, processing, completed, failed
    file_path: Optional[str] = None
    original_filename: Optional[str] = None
    processing_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = datetime.utcnow()

class VoiceCloneStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: Optional[int] = None  # 0-100
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    estimated_completion: Optional[datetime] = None