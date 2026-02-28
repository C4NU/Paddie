import json
import os
from typing import Dict, Optional

class Translator:
    _instance = None
    _current_language = "en"
    _translations: Dict[str, Dict[str, str]] = {}
    _config_file = "user_config/language.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Translator, cls).__new__(cls)
            cls._instance._load_translations()
            cls._instance._load_language_config()
        return cls._instance
    
    def _load_translations(self):
        """번역 파일들을 로드합니다."""
        from resource_path import resource_path
        try:
            locales_dir = resource_path("resources/i18n")
            for filename in os.listdir(locales_dir):
                if filename.endswith(".json"):
                    lang_code = filename[:-5]  # .json 확장자 제거
                    with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                        self._translations[lang_code] = json.load(f)
        except Exception as e:
            print(f"Translation loading failed: {e}")
    
    def _load_language_config(self):
        """저장된 언어 설정을 로드합니다."""
        try:
            if os.path.exists(self._config_file):
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'language' in config and config['language'] in self._translations:
                        self._current_language = config['language']
        except Exception:
            pass
    
    def save_language_config(self):
        """현재 언어 설정을 저장합니다."""
        try:
            os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump({'language': self._current_language}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def set_language(self, language_code: str):
        """현재 언어를 설정합니다."""
        if language_code in self._translations:
            self._current_language = language_code
            self.save_language_config()
            return True
        return False
    
    def get_current_language(self) -> str:
        """현재 설정된 언어 코드를 반환합니다."""
        return self._current_language
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """주어진 키에 대한 번역을 반환합니다."""
        if self._current_language in self._translations:
            return self._translations[self._current_language].get(key, default or key)
        return default or key 