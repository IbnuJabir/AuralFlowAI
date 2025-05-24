# backend/app/services/voice_service.py
import os
import uuid
import tempfile
import requests
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from fastapi import UploadFile, HTTPException
from urllib.parse import urlparse
import mimetypes
import logging

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        self.upload_dir = Path("uploads/voice")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Supported file formats
        self.supported_audio_formats = {
            ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"
        }
        self.supported_video_formats = {
            ".mp4", ".avi", ".mov", ".mkv", ".webm"
        }
        
    async def process_voice_clone_request(
        self, 
        file: Optional[UploadFile] = None,
        link: Optional[str] = None,
        request_type: str = "file",
        source: str = "unknown",
        target_language: str = "en",
        voice_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process voice cloning request from file or URL"""
        
        try:
            if request_type == "file" and file:
                return await self._process_file_upload(file, target_language, voice_settings)
            elif request_type == "link" and link:
                return await self._process_url_download(link, source, target_language, voice_settings)
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid request: either file or link must be provided"
                )
                
        except Exception as e:
            logger.error(f"Error processing voice clone request: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    async def _process_file_upload(
        self, 
        file: UploadFile, 
        target_language: str,
        voice_settings: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process uploaded file"""
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
            
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in (self.supported_audio_formats | self.supported_video_formats):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format: {file_extension}"
            )
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        safe_filename = f"{unique_id}_{file.filename}"
        file_path = self.upload_dir / safe_filename
        
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Get file metadata
        file_size = len(content)
        file_info = {
            "original_filename": file.filename,
            "file_path": str(file_path),
            "file_size": file_size,
            "file_type": file_extension,
            "is_audio": file_extension in self.supported_audio_formats,
            "is_video": file_extension in self.supported_video_formats
        }
        
        return file_info
    
    async def _process_url_download(
        self, 
        url: str, 
        source: str,
        target_language: str,
        voice_settings: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process URL download"""
        
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        try:
            # Download file
            response = requests.head(url, timeout=10)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            file_extension = mimetypes.guess_extension(content_type) or ""
            
            # If we can't determine from content-type, try URL path
            if not file_extension:
                url_path = Path(parsed_url.path)
                file_extension = url_path.suffix.lower()
            
            if file_extension not in (self.supported_audio_formats | self.supported_video_formats):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported content type from URL: {content_type}"
                )
            
            # Download the actual file
            download_response = requests.get(url, timeout=60)
            download_response.raise_for_status()
            
            # Generate unique filename
            unique_id = str(uuid.uuid4())
            filename = f"{unique_id}_downloaded{file_extension}"
            file_path = self.upload_dir / filename
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(download_response.content)
            
            file_info = {
                "original_filename": filename,
                "file_path": str(file_path),
                "file_size": len(download_response.content),
                "file_type": file_extension,
                "source_url": url,
                "source": source,
                "is_audio": file_extension in self.supported_audio_formats,
                "is_video": file_extension in self.supported_video_formats
            }
            
            return file_info
            
        except requests.RequestException as e:
            raise HTTPException(status_code=400, detail=f"Failed to download from URL: {str(e)}")
    
    def cleanup_file(self, file_path: str) -> None:
        """Clean up temporary files"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to cleanup file {file_path}: {str(e)}")
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get metadata for processed file"""
        if not os.path.exists(file_path):
            return {}
            
        stat = os.stat(file_path)
        return {
            "file_size": stat.st_size,
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime
        }