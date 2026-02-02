from languages.id.user import IndonesianUserMessageTranslator
from languages.id.error import IndonesianErrorMessageTranslator

class IndonesianMessageLanguage(IndonesianUserMessageTranslator, IndonesianErrorMessageTranslator):
    def __init__(self) -> None:
        super().__init__()
