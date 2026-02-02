from typing import Union, Any
from languages.en import EnglishMessageLanguage
from languages.id import IndonesianMessageLanguage

LANGUAGE_MAP: dict[str, Any] = {
    "en": EnglishMessageLanguage,
    "id": IndonesianMessageLanguage,
}


def get_translator(lang: str = "en") -> Union[EnglishMessageLanguage, IndonesianMessageLanguage]:
    translator_class = LANGUAGE_MAP.get(lang, EnglishMessageLanguage)
    return translator_class()
