# backend/workers/tasks/audio_tasks.py
from celery import current_task
from workers.celery_app import celery_app
from typing import Dict, Any, Optional
import logging
import os
import time
from pathlib import Path

# Import the actual service implementations
from workers.services.audio_service import AudioService
from workers.services.speech_service import SpeechService
from workers.services.translation_service import TranslationService
from workers.services.tts_service import TTSService
from workers.services.audio_mixing_service import AudioMixingService

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def process_voice_cloning_task(
    self,
    file_path: str,
    target_language: str = "en",
    voice_settings: Dict[str, Any] = None,
    file_info: Dict[str, Any] = None
):
    """
    Background task for processing voice cloning with real ML implementations
    """
    processing_files = []  # Track files for cleanup
    
    try:
        logger.info(f"Starting voice cloning task for file: {file_path}")
        start_time = time.time()
        
        # Update task state
        self.update_state(
            state='PROGRESS',
            meta={'progress': 10, 'status': 'Initializing voice cloning pipeline'}
        )
        
        # Initialize services
        audio_service = AudioService()
        speech_service = SpeechService()
        translation_service = TranslationService()
        tts_service = TTSService()
        mixing_service = AudioMixingService()
        
        # Initialize output path
        input_path = Path(file_path)
        output_dir = input_path.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Step 1: Audio preprocessing and validation
        self.update_state(
            state='PROGRESS',
            meta={'progress': 15, 'status': 'Validating input file'}
        )
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        processing_file_path = file_path
        
        # Step 2: Extract audio from video if needed
        if file_info and file_info.get("is_video", False):
            self.update_state(
                state='PROGRESS',
                meta={'progress': 25, 'status': 'Extracting audio from video'}
            )
            
            extracted_audio_path = audio_service.extract_audio_from_video(file_path)
            processing_file_path = extracted_audio_path
            processing_files.append(extracted_audio_path)
            logger.info(f"Audio extracted to: {extracted_audio_path}")
        
        # Step 3: Separate vocals from background
        self.update_state(
            state='PROGRESS',
            meta={'progress': 35, 'status': 'Separating vocals from background music'}
        )
        
        vocals_path = audio_service.separate_vocals(processing_file_path)
        processing_files.append(vocals_path)
        logger.info(f"Vocals separated to: {vocals_path}")
        
        # Step 4: Extract background audio for later mixing
        background_path = mixing_service.extract_background_audio(processing_file_path, vocals_path)
        processing_files.append(background_path)
        
        # Step 5: Speech recognition/transcription
        self.update_state(
            state='PROGRESS',
            meta={'progress': 50, 'status': 'Transcribing speech to text'}
        )
        
        transcription_result = speech_service.transcribe_audio(vocals_path)
        original_text = transcription_result["text"]
        detected_language = transcription_result["language"]
        
        logger.info(f"Transcription completed. Detected language: {detected_language}")
        logger.info(f"Original text: {original_text[:100]}...")
        
        # Step 6: Translation (if needed)
        translated_text = original_text
        if target_language != "auto" and target_language != detected_language:
            self.update_state(
                state='PROGRESS',
                meta={'progress': 65, 'status': f'Translating to {target_language}'}
            )
            
            translated_text = translation_service.translate_text(
                original_text, 
                detected_language, 
                target_language
            )
            logger.info(f"Translation completed: {translated_text[:100]}...")
        
        # Step 7: Voice cloning/synthesis
        self.update_state(
            state='PROGRESS',
            meta={'progress': 75, 'status': 'Generating speech with voice cloning'}
        )
        
        cloned_audio_path = tts_service.clone_voice_with_text(
            reference_audio_path=vocals_path,
            text=translated_text,
            target_language=target_language,
            voice_settings=voice_settings or {}
        )
        processing_files.append(cloned_audio_path)
        logger.info(f"Voice cloning completed: {cloned_audio_path}")
        
        # Step 8: Mix cloned vocals with background audio
        self.update_state(
            state='PROGRESS',
            meta={'progress': 85, 'status': 'Mixing audio with background'}
        )
        
        # Set mixing volumes from voice settings
        vocal_volume = voice_settings.get("vocal_volume", 1.0) if voice_settings else 1.0
        bg_volume = voice_settings.get("background_volume", 0.3) if voice_settings else 0.3
        
        mixed_audio_filename = f"mixed_{input_path.stem}_{target_language}.wav"
        mixed_audio_path = output_dir / mixed_audio_filename
        
        final_audio_path = mixing_service.mix_audio_with_background(
            vocals_path=vocals_path,
            background_path=background_path,
            new_vocals_path=cloned_audio_path,
            output_path=str(mixed_audio_path),
            vocal_volume=vocal_volume,
            background_volume=bg_volume
        )
        
        # Step 9: Create final output (video or audio)
        self.update_state(
            state='PROGRESS',
            meta={'progress': 95, 'status': 'Creating final output'}
        )
        
        if file_info and file_info.get("is_video", False):
            # Sync audio with original video
            final_output_filename = f"dubbed_{input_path.stem}_{target_language}.mp4"
            final_output_path = output_dir / final_output_filename
            
            final_result_path = mixing_service.sync_audio_to_video(
                video_path=file_path,
                audio_path=final_audio_path,
                output_path=str(final_output_path)
            )
        else:
            # For audio-only files, the mixed audio is the final result
            final_result_path = final_audio_path
        
        # Step 10: Calculate processing stats
        processing_time = time.time() - start_time
        output_file_size = os.path.getsize(final_result_path) if os.path.exists(final_result_path) else 0
        
        # Prepare final result
        result = {
            "success": True,
            "output_path": str(final_result_path),
            "original_text": original_text,
            "translated_text": translated_text,
            "detected_language": detected_language,
            "target_language": target_language,
            "processing_time": round(processing_time, 2),
            "file_info": {
                "output_filename": Path(final_result_path).name,
                "file_size": output_file_size,
                "is_video": file_info.get("is_video", False) if file_info else False,
                "original_filename": file_info.get("original_filename", "") if file_info else ""
            },
            "transcription": {
                "segments": transcription_result.get("segments", []),
                "confidence": transcription_result.get("confidence", 0.0)
            }
        }
        
        logger.info(f"Voice cloning task completed successfully in {processing_time:.2f}s")
        logger.info(f"Final output: {final_result_path}")
        
        # Cleanup temporary files
        cleanup_temp_files(processing_files)
        
        return result
        
    except Exception as e:
        logger.error(f"Voice cloning task failed: {str(e)}")
        
        # Cleanup on failure
        cleanup_temp_files(processing_files + [file_path])
        
        self.update_state(
            state='FAILURE',
            meta={
                'error': str(e),
                'progress': 0,
                'status': f'Failed: {str(e)}'
            }
        )
        raise e

def cleanup_temp_files(file_paths: list):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                # Only remove files in temp/processing directories or with specific patterns
                path_obj = Path(file_path)
                if ("temp" in str(path_obj) or 
                    "extracted" in path_obj.name or 
                    "vocals" in path_obj.name or 
                    "background" in path_obj.name or
                    "cloned" in path_obj.name):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to cleanup {file_path}: {e}")

def get_audio_duration(audio_path: str) -> float:
    """Get duration of audio file in seconds"""
    try:
        import torchaudio
        info = torchaudio.info(audio_path)
        return info.num_frames / info.sample_rate
    except Exception as e:
        logger.error(f"Failed to get audio duration: {e}")
        return 0.0