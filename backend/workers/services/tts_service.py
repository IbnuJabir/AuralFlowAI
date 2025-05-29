# backend/workers/services/tts_service.py
import torch
import torchaudio
from TTS.api import TTS
import tempfile
import os
from pathlib import Path
import logging
from typing import Optional, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_model = None
        self.vocoder_model = None
        
    def initialize_tts(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        """Initialize TTS model"""
        try:
            if self.tts_model is None:
                logger.info(f"Loading TTS model: {model_name}")
                self.tts_model = TTS(model_name).to(self.device)
                logger.info("TTS model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load TTS model: {e}")
            # Fallback to a simpler model
            try:
                self.tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(self.device)
                logger.info("Loaded fallback TTS model")
            except Exception as e2:
                logger.error(f"Failed to load fallback TTS model: {e2}")
                raise Exception(f"Could not initialize any TTS model: {e2}")
    
    def clone_voice_with_text(
        self, 
        reference_audio_path: str, 
        text: str, 
        target_language: str = "en",
        voice_settings: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate speech with voice cloning
        """
        try:
            self.initialize_tts()
            
            # Create output path
            output_dir = Path(reference_audio_path).parent
            output_filename = f"cloned_speech_{Path(reference_audio_path).stem}.wav"
            output_path = output_dir / output_filename
            
            # Voice settings
            settings = voice_settings or {}
            speed = settings.get("speed", 1.0)
            
            # Use XTTS for multilingual voice cloning
            if hasattr(self.tts_model, 'tts_to_file'):
                self.tts_model.tts_to_file(
                    text=text,
                    speaker_wav=reference_audio_path,
                    language=target_language,
                    file_path=str(output_path)
                )
            else:
                # Fallback for simpler TTS models
                wav = self.tts_model.tts(text=text)
                
                # Convert to tensor if needed
                if isinstance(wav, list):
                    wav = torch.tensor(wav)
                elif isinstance(wav, np.ndarray):
                    wav = torch.from_numpy(wav)
                
                # Ensure correct shape
                if wav.dim() == 1:
                    wav = wav.unsqueeze(0)
                
                # Save audio
                torchaudio.save(str(output_path), wav, 22050)
            
            # Apply speed adjustment if needed
            if speed != 1.0:
                output_path = self._adjust_speed(str(output_path), speed)
            
            logger.info(f"Voice cloning completed: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Voice cloning failed: {str(e)}")
            # Generate fallback TTS without voice cloning
            return self._generate_fallback_tts(text, target_language, reference_audio_path)
    
    def _generate_fallback_tts(self, text: str, language: str, reference_path: str) -> str:
        """Generate basic TTS without voice cloning as fallback"""
        try:
            # Use basic TTS
            output_dir = Path(reference_path).parent  
            output_path = output_dir / f"fallback_tts_{Path(reference_path).stem}.wav"
            
            # Simple TTS generation
            if self.tts_model is None:
                self.tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(self.device)
            
            wav = self.tts_model.tts(text=text)
            
            # Convert and save
            if isinstance(wav, list):
                wav = torch.tensor(wav)
            elif isinstance(wav, np.ndarray):
                wav = torch.from_numpy(wav)
                
            if wav.dim() == 1:
                wav = wav.unsqueeze(0)
                
            torchaudio.save(str(output_path), wav, 22050)
            
            logger.info(f"Fallback TTS generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Fallback TTS failed: {e}")
            raise Exception(f"All TTS methods failed: {e}")
    
    def _adjust_speed(self, audio_path: str, speed: float) -> str:
        """Adjust audio playback speed"""
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Apply speed change using torchaudio
            effects = [
                ["speed", str(speed)],
                ["rate", str(sample_rate)]
            ]
            
            waveform_adjusted, _ = torchaudio.sox_effects.apply_effects_tensor(
                waveform, sample_rate, effects
            )
            
            # Save adjusted audio
            speed_adjusted_path = audio_path.replace(".wav", f"_speed_{speed}.wav")
            torchaudio.save(speed_adjusted_path, waveform_adjusted, sample_rate)
            
            # Remove original and rename
            os.remove(audio_path)
            os.rename(speed_adjusted_path, audio_path)
            
            return audio_path
            
        except Exception as e:
            logger.warning(f"Speed adjustment failed: {e}")
            return audio_path  # Return original if adjustment fails
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages for TTS"""
        return [
            "en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", 
            "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"
        ]