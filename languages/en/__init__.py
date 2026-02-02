from languages.en.user import EnglishUserMessageTranslator
from languages.en.error import EnglishErrorMessageTranslator


class EnglishMessageLanguage(EnglishUserMessageTranslator, EnglishErrorMessageTranslator):
    def __init__(self) -> None:
        super().__init__()
