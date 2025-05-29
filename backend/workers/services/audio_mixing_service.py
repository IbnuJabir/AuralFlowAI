# backend/workers/services/audio_mixing_service.py
import torch
import torchaudio
import numpy as np
from pathlib import Path
import logging
from typing import Tuple, Optional
import subprocess

logger = logging.getLogger(__name__)

class AudioMixingService:
    
    @staticmethod
    def mix_audio_with_background(
        vocals_path: str,
        background_path: str, 
        new_vocals_path: str,
        output_path: str,
        vocal_volume: float = 1.0,
        background_volume: float = 0.3
    ) -> str:
        """
        Mix new vocals with original background audio
        """
        try:
            # Load audio files
            new_vocals, vocal_sr = torchaudio.load(new_vocals_path)
            background, bg_sr = torchaudio.load(background_path)
            
            # Ensure same sample rate
            if vocal_sr != bg_sr:
                # Resample vocals to match background
                resampler = torchaudio.transforms.Resample(vocal_sr, bg_sr)
                new_vocals = resampler(new_vocals)
                vocal_sr = bg_sr
            
            # Ensure same number of channels
            if new_vocals.shape[0] != background.shape[0]:
                if new_vocals.shape[0] == 1 and background.shape[0] == 2:
                    # Convert mono vocals to stereo
                    new_vocals = new_vocals.repeat(2, 1)
                elif new_vocals.shape[0] == 2 and background.shape[0] == 1:
                    # Convert stereo vocals to mono
                    new_vocals = torch.mean(new_vocals, dim=0, keepdim=True)
            
            # Match lengths - pad or trim as needed
            vocals_length = new_vocals.shape[1]
            bg_length = background.shape[1]
            
            if vocals_length > bg_length:
                # Trim vocals to match background
                new_vocals = new_vocals[:, :bg_length]
            elif vocals_length < bg_length:
                # Pad vocals with silence
                padding = bg_length - vocals_length
                new_vocals = torch.nn.functional.pad(new_vocals, (0, padding))
            
            # Apply volume adjustments
            new_vocals = new_vocals * vocal_volume
            background = background * background_volume
            
            # Mix the audio
            mixed_audio = new_vocals + background
            
            # Normalize to prevent clipping
            max_val = torch.max(torch.abs(mixed_audio))
            if max_val > 0.95:
                mixed_audio = mixed_audio / max_val * 0.95
            
            # Save mixed audio
            torchaudio.save(output_path, mixed_audio, vocal_sr)
            
            logger.info(f"Audio mixing completed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio mixing failed: {str(e)}")
            # Fallback: just use the new vocals
            return AudioMixingService._fallback_audio_copy(new_vocals_path, output_path)
    
    @staticmethod 
    def extract_background_audio(original_audio_path: str, vocals_path: str) -> str:
        """
        Extract background audio by subtracting vocals from original
        """
        try:
            # Load original and vocals
            original, orig_sr = torchaudio.load(original_audio_path)
            vocals, vocal_sr = torchaudio.load(vocals_path)
            
            # Ensure same sample rate
            if vocal_sr != orig_sr:
                resampler = torchaudio.transforms.Resample(vocal_sr, orig_sr)
                vocals = resampler(vocals)
            
            # Ensure same channels and length
            if vocals.shape[0] != original.shape[0]:
                if vocals.shape[0] == 1 and original.shape[0] == 2:
                    vocals = vocals.repeat(2, 1)
                elif vocals.shape[0] == 2 and original.shape[0] == 1:
                    vocals = torch.mean(vocals, dim=0, keepdim=True)
            
            # Match lengths
            min_length = min(original.shape[1], vocals.shape[1])
            original = original[:, :min_length]
            vocals = vocals[:, :min_length]
            
            # Extract background (subtract vocals)
            background = original - vocals
            
            # Apply some smoothing to reduce artifacts
            background = AudioMixingService._apply_smoothing(background)
            
            # Save background audio
            background_path = str(Path(original_audio_path).with_stem(
                f"{Path(original_audio_path).stem}_background"
            ))
            torchaudio.save(background_path, background, orig_sr)
            
            return background_path
            
        except Exception as e:
            logger.error(f"Background extraction failed: {str(e)}")
            # Return original audio as fallback
            return original_audio_path
    
    @staticmethod
    def _apply_smoothing(audio: torch.Tensor, kernel_size: int = 5) -> torch.Tensor:
        """Apply smoothing to reduce audio artifacts"""
        try:
            # Simple moving average filter
            kernel = torch.ones(kernel_size) / kernel_size
            
            smoothed_channels = []
            for channel in range(audio.shape[0]):
                # Apply 1D convolution for smoothing
                smoothed = torch.nn.functional.conv1d(
                    audio[channel:channel+1].unsqueeze(0), 
                    kernel.unsqueeze(0).unsqueeze(0),
                    padding=kernel_size//2
                ).squeeze()
                smoothed_channels.append(smoothed)
            
            return torch.stack(smoothed_channels)
            
        except Exception as e:
            logger.warning(f"Audio smoothing failed: {e}")
            return audio
    
    @staticmethod
    def _fallback_audio_copy(source_path: str, destination_path: str) -> str:
        """Fallback: copy source audio to destination"""
        try:
            import shutil
            shutil.copy2(source_path, destination_path)
            logger.info(f"Audio copied as fallback: {destination_path}")
            return destination_path
        except Exception as e:
            logger.error(f"Fallback audio copy failed: {e}")
            return source_path
    
    @staticmethod
    def sync_audio_to_video(video_path: str, audio_path: str, output_path: str) -> str:
        """
        Sync new audio with original video using FFmpeg
        """
        try:
            # Use FFmpeg to replace audio in video
            cmd = [
                "ffmpeg",
                "-i", video_path,      # Input video
                "-i", audio_path,      # Input audio  
                "-c:v", "copy",        # Copy video stream
                "-c:a", "aac",         # Encode audio as AAC
                "-b:a", "192k",        # Audio bitrate
                "-map", "0:v:0",       # Map video from first input
                "-map", "1:a:0",       # Map audio from second input
                "-shortest",           # Match shortest stream duration
                "-y",                  # Overwrite output
                output_path
            ]
            
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            logger.info(f"Video-audio sync completed: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e.stderr}")
            raise Exception(f"Video sync failed: {e.stderr}")
        except Exception as e:
            logger.error(f"Video sync error: {str(e)}")
            raise Exception(f"Video sync failed: {str(e)}")
    
    @staticmethod
    def normalize_audio_levels(audio_path: str, target_db: float = -20.0) -> str:
        """
        Normalize audio levels to target dB
        """
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Calculate current RMS level
            rms = torch.sqrt(torch.mean(waveform ** 2))
            current_db = 20 * torch.log10(rms + 1e-8)
            
            # Calculate gain needed
            gain_db = target_db - current_db
            gain_linear = 10 ** (gain_db / 20)
            
            # Apply gain
            waveform_normalized = waveform * gain_linear
            
            # Prevent clipping
            max_val = torch.max(torch.abs(waveform_normalized))
            if max_val > 0.95:
                waveform_normalized = waveform_normalized / max_val * 0.95
            
            # Save normalized audio
            normalized_path = audio_path.replace(".wav", "_normalized.wav")
            torchaudio.save(normalized_path, waveform_normalized, sample_rate)
            
            return normalized_path
            
        except Exception as e:
            logger.warning(f"Audio normalization failed: {e}")
            return audio_path