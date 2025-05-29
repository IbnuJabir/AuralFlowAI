# backend/workers/services/audio_service.py
import subprocess
import torch
import torchaudio
from demucs.pretrained import get_model
from demucs.apply import apply_model
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class AudioService:
    @staticmethod
    def extract_audio_from_video(video_path: str) -> str:
        """Real implementation using FFmpeg"""
        output_path = str(Path(video_path).with_suffix(".wav"))
        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "2",
            "-y",
            output_path
        ], check=True)
        return output_path

    @staticmethod
    def separate_vocals(audio_path: str) -> str:
        """Real implementation using Demucs"""
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = get_model('htdemucs').to(device)
        wav, sr = torchaudio.load(audio_path)
        
        if wav.shape[0] == 1:
            wav = torch.cat([wav, wav])
            
        wav = wav.unsqueeze(0).to(device)
        with torch.no_grad():
            sources = apply_model(model, wav)[0]
            
        vocals_path = str(Path(audio_path).with_stem(f"{Path(audio_path).stem}_vocals"))
        torchaudio.save(vocals_path, sources[0].cpu(), sr)
        return vocals_path