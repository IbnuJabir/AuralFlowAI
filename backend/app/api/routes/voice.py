# backend/app/api/routes/voice.py
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from app.schemas.responses.voice import VoiceCloneResponse, VoiceCloneStatusResponse
from app.services.voice_service import VoiceService
from workers.tasks.audio_tasks import process_voice_cloning_task

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/voice", tags=["voice"])

# Dependency to get voice service
def get_voice_service() -> VoiceService:
    return VoiceService()

@router.post("/voice-clone", response_model=VoiceCloneResponse)
async def voice_clone_endpoint(
    background_tasks: BackgroundTasks,
    type: str = Form(...),
    source: Optional[str] = Form("unknown"),
    target_language: Optional[str] = Form("en"),
    voice_settings: Optional[str] = Form(None),  # JSON string
    file: Optional[UploadFile] = File(None),
    link: Optional[str] = Form(None),
    voice_service: VoiceService = Depends(get_voice_service)
):
    """
    Voice cloning endpoint that accepts either file upload or URL link
    """
    
    try:
        logger.info(f"Received voice clone request - type: {type}, source: {source}")
        
        # Validate request
        if type not in ["file", "link"]:
            raise HTTPException(
                status_code=400,
                detail="Type must be either 'file' or 'link'"
            )
        
        if type == "file" and not file:
            raise HTTPException(
                status_code=400,
                detail="File is required when type is 'file'"
            )
            
        if type == "link" and not link:
            raise HTTPException(
                status_code=400,
                detail="Link is required when type is 'link'"
            )
        
        # Parse voice settings if provided
        parsed_voice_settings = None
        if voice_settings:
            try:
                import json
                parsed_voice_settings = json.loads(voice_settings)
            except json.JSONDecodeError:
                logger.warning("Invalid voice_settings JSON, using defaults")
        
        # Process the request
        file_info = await voice_service.process_voice_clone_request(
            file=file,
            link=link,
            request_type=type,
            source=source,
            target_language=target_language,
            voice_settings=parsed_voice_settings
        )
        
        # Create task for background processing
        task_result = process_voice_cloning_task.delay(
            file_path=file_info["file_path"],
            target_language=target_language,
            voice_settings=parsed_voice_settings or {},
            file_info=file_info
        )
        
        # Prepare response
        response_data = VoiceCloneResponse(
            success=True,
            message="Voice cloning request submitted successfully",
            task_id=task_result.id,
            status="submitted",
            file_path=file_info["file_path"],
            original_filename=file_info.get("original_filename"),
            metadata={
                "file_size": file_info.get("file_size"),
                "file_type": file_info.get("file_type"),
                "is_audio": file_info.get("is_audio", False),
                "is_video": file_info.get("is_video", False),
                "source": source,
                "target_language": target_language
            }
        )
        
        logger.info(f"Voice clone task created with ID: {task_result.id}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in voice clone endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/status/{task_id}", response_model=VoiceCloneStatusResponse)
async def get_voice_clone_status(task_id: str):
    """
    Get the status of a voice cloning task
    """
    try:
        from workers.celery_app import celery_app
        
        # Get task result
        task_result = celery_app.AsyncResult(task_id)
        
        if not task_result:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        
        # Determine status
        status = task_result.status.lower()
        
        response = VoiceCloneStatusResponse(
            task_id=task_id,
            status=status
        )
        
        if status == "success":
            result = task_result.result
            response.result_url = result.get("output_path") if result else None
            response.progress = 100
            
        elif status == "failure":
            response.error_message = str(task_result.info) if task_result.info else "Unknown error"
            response.progress = 0
            
        elif status == "pending":
            response.progress = 0
            
        else:  # processing states
            # Get progress info if available
            if hasattr(task_result, 'info') and isinstance(task_result.info, dict):
                response.progress = task_result.info.get('progress', 0)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task status: {str(e)}"
        )

@router.delete("/task/{task_id}")
async def cancel_voice_clone_task(
    task_id: str,
    voice_service: VoiceService = Depends(get_voice_service)
):
    """
    Cancel a voice cloning task
    """
    try:
        from workers.celery_app import celery_app
        
        # Revoke the task
        celery_app.control.revoke(task_id, terminate=True)
        
        return JSONResponse(
            content={
                "success": True,
                "message": f"Task {task_id} cancelled successfully"
            }
        )
        
    except Exception as e:
        logger.error(f"Error cancelling task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cancel task: {str(e)}"
        )

@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported audio and video formats
    """
    return {
        "audio_formats": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "video_formats": [".mp4", ".avi", ".mov", ".mkv", ".webm"],
        "max_file_size": "100MB",  # You can configure this
        "supported_languages": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko"]  # Add your supported languages
    }