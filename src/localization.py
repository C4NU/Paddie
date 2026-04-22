from PySide6.QtCore import QLocale, QTranslator

from resource_path import resource_path
from user_config import UserConfig


LANGUAGE_CODES = {
    1: "ko",
    2: "ja",
    3: "zh",
    4: "en",
}
SYSTEM_LANGUAGE_CODES = {"ko", "ja", "zh", "en"}

translator = None
current_language_code = None


def resolve_language_code(language_index):
    if language_index in LANGUAGE_CODES:
        return LANGUAGE_CODES[language_index]

    system_code = QLocale.system().name()[:2]
    if system_code in SYSTEM_LANGUAGE_CODES:
        return system_code

    return "en"


def install_translator(app):
    UserConfig.load()
    return apply_language(app, UserConfig.language, save=False)


def apply_language(app, language_index, save=True):
    global translator
    global current_language_code

    if translator is not None:
        app.removeTranslator(translator)
        translator = None

    language_code = resolve_language_code(language_index)
    if language_code == "en":
        current_language_code = language_code
        if save:
            UserConfig.language = language_index
            UserConfig.save()
        return language_code

    translator = QTranslator()
    translation_path = resource_path(f"resources/i18n/translations_{language_code}.qm")
    if translator.load(translation_path):
        app.installTranslator(translator)
        current_language_code = language_code
        if save:
            UserConfig.language = language_index
            UserConfig.save()
        return language_code

    if language_code != "en":
        fallback_path = resource_path("resources/i18n/translations_en.qm")
        if translator.load(fallback_path):
            app.installTranslator(translator)
            current_language_code = "en"
            if save:
                UserConfig.language = language_index
                UserConfig.save()
            return "en"

    current_language_code = None
    return None


def get_current_language_code():
    return current_language_code or resolve_language_code(UserConfig.language)
