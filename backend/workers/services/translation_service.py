# backend/workers/services/translation_service.py
from transformers import MarianMTModel, MarianTokenizer, pipeline
import torch
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}  # Cache for loaded models
        self.tokenizers = {}
        
        # Language code mappings
        self.lang_codes = {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "ru": "Russian",
            "hi": "Hindi"
        }
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language
        """
        try:
            if source_lang == target_lang:
                return text
                
            # For complex translation pairs, use pipeline approach
            if self._use_pipeline_translation(source_lang, target_lang):
                return self._translate_with_pipeline(text, source_lang, target_lang)
            else:
                return self._translate_with_marian(text, source_lang, target_lang)
                
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Fallback: return original text with language indicator
            return f"[{target_lang.upper()}] {text}"
    
    def _use_pipeline_translation(self, source_lang: str, target_lang: str) -> bool:
        """Determine if we should use pipeline vs Marian models"""
        # Use pipeline for more complex language pairs
        complex_pairs = ["zh", "ja", "ko", "ar", "hi", "ru"]
        return source_lang in complex_pairs or target_lang in complex_pairs
    
    def _translate_with_pipeline(self, text: str, source_lang: str, target_lang: str) -> str:
        """Use Hugging Face translation pipeline"""
        try:
            # Create translation pipeline
            translator = pipeline(
                "translation",
                model=f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}",
                device=0 if self.device == "cuda" else -1
            )
            
            # Split long text into chunks
            chunks = self._split_text(text, max_length=500)
            translated_chunks = []
            
            for chunk in chunks:
                if chunk.strip():
                    result = translator(chunk, max_length=512)
                    translated_chunks.append(result[0]['translation_text'])
            
            return " ".join(translated_chunks)
            
        except Exception as e:
            logger.warning(f"Pipeline translation failed, trying alternative: {e}")
            return self._translate_with_marian_fallback(text, source_lang, target_lang)
    
    def _translate_with_marian(self, text: str, source_lang: str, target_lang: str) -> str:
        """Use Marian MT models for translation"""
        try:
            model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
            
            # Load model and tokenizer if not cached
            if model_name not in self.models:
                logger.info(f"Loading translation model: {model_name}")
                self.tokenizers[model_name] = MarianTokenizer.from_pretrained(model_name)
                self.models[model_name] = MarianMTModel.from_pretrained(model_name).to(self.device)
            
            tokenizer = self.tokenizers[model_name]
            model = self.models[model_name]
            
            # Split text into manageable chunks
            chunks = self._split_text(text, max_length=400)
            translated_chunks = []
            
            for chunk in chunks:
                if chunk.strip():
                    # Tokenize
                    inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                    
                    # Generate translation
                    with torch.no_grad():
                        translated = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
                    
                    # Decode
                    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
                    translated_chunks.append(translated_text)
            
            return " ".join(translated_chunks)
            
        except Exception as e:
            logger.error(f"Marian translation failed: {e}")
            return self._translate_with_marian_fallback(text, source_lang, target_lang)
    
    def _translate_with_marian_fallback(self, text: str, source_lang: str, target_lang: str) -> str:
        """Fallback translation using English as intermediate language"""
        try:
            if source_lang != "en":
                # First translate to English
                english_text = self._translate_with_marian(text, source_lang, "en")
                if target_lang != "en":
                    # Then translate from English to target
                    return self._translate_with_marian(english_text, "en", target_lang)
                return english_text
            else:
                # Direct translation from English
                return self._translate_with_marian(text, "en", target_lang)
                
        except Exception as e:
            logger.error(f"Fallback translation failed: {e}")
            return f"[Translation Error - {target_lang.upper()}] {text}"
    
    def _split_text(self, text: str, max_length: int = 400) -> List[str]:
        """Split text into chunks for translation"""
        sentences = text.split(". ")
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text]
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported language codes and names"""
        return self.lang_codes