#!/usr/bin/env python3
"""
Language Settings Service - Manages dynamic language switching
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from frontend.core.logging_config import game_logger


@dataclass
class LanguageOption:
    """Represents a language option"""
    code: str
    name: str
    native_name: str
    flag: str = ""


class LanguageService:
    """Service for managing language settings and switching"""
    
    # Available languages
    SUPPORTED_LANGUAGES = [
        LanguageOption(
            code="english",
            name="English",
            native_name="English",
            flag="🇺🇸"
        ),
        LanguageOption(
            code="chinese_simplified",
            name="Chinese (Simplified)",
            native_name="简体中文 - Chinese (Simplified)",
            flag=""
        ),
        LanguageOption(
            code="spanish",
            name="Spanish",
            native_name="Español - Spanish",
            flag="🇪🇸"
        ),
        LanguageOption(
            code="french",
            name="French",
            native_name="Français - French",
            flag="🇫🇷"
        ),
        LanguageOption(
            code="german",
            name="German",
            native_name="Deutsch - German",
            flag="🇩🇪"
        ),
        LanguageOption(
            code="japanese",
            name="Japanese",
            native_name="日本語 - Japanese",
            flag="🇯🇵"
        ),
        LanguageOption(
            code="portuguese",
            name="Portuguese",
            native_name="Português - Portuguese",
            flag="🇵🇹"
        ),
        LanguageOption(
            code="italian",
            name="Italian",
            native_name="Italiano - Italian",
            flag="🇮🇹"
        ),
        LanguageOption(
            code="russian",
            name="Russian",
            native_name="Русский - Russian",
            flag="🇷🇺"
        ),
        LanguageOption(
            code="korean",
            name="Korean",
            native_name="한국어 - Korean",
            flag="🇰🇷"
        ),
    ]
    
    DEFAULT_LANGUAGE = "english"
    SETTINGS_FILE = Path("user_settings.json")
    
    def __init__(self):
        self._current_language: str = self._load_language_preference()
        game_logger.info("Language service initialized", current_language=self._current_language)
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self._current_language
    
    def get_current_language_display(self) -> str:
        """Get current language display name with flag"""
        lang_option = self.get_language_option(self._current_language)
        if lang_option:
            return f"{lang_option.flag} {lang_option.native_name}"
        return f"🌐 {self._current_language.title()}"
    
    def get_language_option(self, code: str) -> Optional[LanguageOption]:
        """Get language option by code"""
        for lang in self.SUPPORTED_LANGUAGES:
            if lang.code == code:
                return lang
        return None
    
    def get_language_choices(self) -> List[Tuple[str, str]]:
        """Get language choices for Gradio dropdown"""
        choices = []
        for lang in self.SUPPORTED_LANGUAGES:
            display_name = f"{lang.flag} {lang.native_name}"
            choices.append((display_name, lang.code))
        return choices
    
    def set_language(self, language_code: str) -> bool:
        """
        Set current language and save preference
        
        Args:
            language_code: Language code to set
            
        Returns:
            True if language was changed successfully
        """
        # Validate language code
        if not self.get_language_option(language_code):
            game_logger.warning("Invalid language code attempted", language_code=language_code)
            return False
        
        old_language = self._current_language
        self._current_language = language_code
        
        # Save preference
        self._save_language_preference()
        
        # Update environment variable for AI prompts
        os.environ["LANGUAGE"] = language_code
        
        game_logger.info(
            "Language changed",
            old_language=old_language,
            new_language=language_code
        )
        
        return True
    
    def _load_language_preference(self) -> str:
        """Load language preference from settings file or environment"""
        try:
            # First try to load from user settings file
            if self.SETTINGS_FILE.exists():
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    saved_language = settings.get("language", self.DEFAULT_LANGUAGE)
                    
                    # Validate saved language
                    if self.get_language_option(saved_language):
                        game_logger.debug("Loaded language from settings", language=saved_language)
                        return saved_language
            
            # Fallback to environment variable
            env_language = os.getenv("LANGUAGE", self.DEFAULT_LANGUAGE).lower()
            if self.get_language_option(env_language):
                game_logger.debug("Using language from environment", language=env_language)
                return env_language
            
            # Final fallback to default
            game_logger.debug("Using default language", language=self.DEFAULT_LANGUAGE)
            return self.DEFAULT_LANGUAGE
            
        except Exception as e:
            game_logger.error("Error loading language preference", error=str(e))
            return self.DEFAULT_LANGUAGE
    
    def _save_language_preference(self) -> None:
        """Save language preference to settings file"""
        try:
            # Load existing settings or create new
            settings = {}
            if self.SETTINGS_FILE.exists():
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            # Update language setting
            settings["language"] = self._current_language
            settings["last_updated"] = str(Path(__file__).stat().st_mtime)
            
            # Save settings
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            game_logger.debug("Language preference saved", language=self._current_language)
            
        except Exception as e:
            game_logger.error("Error saving language preference", error=str(e))
    
    def get_language_info(self) -> Dict[str, str]:
        """Get current language information for display"""
        lang_option = self.get_language_option(self._current_language)
        if lang_option:
            return {
                "code": lang_option.code,
                "name": lang_option.name,
                "native_name": lang_option.native_name,
                "flag": lang_option.flag,
                "display": f"{lang_option.flag} {lang_option.native_name}"
            }
        return {
            "code": self._current_language,
            "name": self._current_language.title(),
            "native_name": self._current_language.title(),
            "flag": "🌐",
            "display": f"🌐 {self._current_language.title()}"
        }


# Global service instance
_language_service = None


def get_language_service() -> LanguageService:
    """Get or create global language service instance"""
    global _language_service
    if _language_service is None:
        _language_service = LanguageService()
    return _language_service


def get_current_language() -> str:
    """Convenience function to get current language"""
    return get_language_service().get_current_language()


def set_language(language_code: str) -> bool:
    """Convenience function to set language"""
    return get_language_service().set_language(language_code)


def get_language_display() -> str:
    """Convenience function to get language display name"""
    return get_language_service().get_current_language_display()