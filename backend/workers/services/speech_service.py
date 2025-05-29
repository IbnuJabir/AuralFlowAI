# backend/workers/services/speech_service.py
import whisper
import torch
from pathlib import Path
import logging
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        
    def load_model(self, model_size: str = "base") -> None:
        """Load Whisper model"""
        if self.model is None:
            logger.info(f"Loading Whisper model '{model_size}' on {self.device}")
            self.model = whisper.load_model(model_size, device=self.device)
    
    def transcribe_audio(self, audio_path: str, language: str = None) -> Dict[str, Any]:
        """
        Transcribe audio file to text using OpenAI Whisper
        """
        try:
            self.load_model()
            
            # Transcribe with optional language specification
            options = {}
            if language and language != "auto":
                options["language"] = language
                
            result = self.model.transcribe(
                audio_path,
                **options,
                word_timestamps=True,
                verbose=False
            )
            
            # Extract segments with timestamps
            segments = []
            for segment in result.get("segments", []):
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "words": segment.get("words", [])
                })
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "segments": segments,
                "confidence": self._calculate_confidence(result)
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise Exception(f"Speech recognition failed: {str(e)}")
    
    def _calculate_confidence(self, result: dict) -> float:
        """Calculate average confidence from segments"""
        try:
            segments = result.get("segments", [])
            if not segments:
                return 0.0
                
            total_confidence = 0.0
            total_words = 0
            
            for segment in segments:
                words = segment.get("words", [])
                for word in words:
                    if "probability" in word:
                        total_confidence += word["probability"]
                        total_words += 1
            
            return total_confidence / total_words if total_words > 0 else 0.8
            
        except Exception:
            return 0.8  # Default confidence