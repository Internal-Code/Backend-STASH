from languages.en.base import EnglishBaseMessageTranslator


class EnglishUserMessageTranslator(EnglishBaseMessageTranslator):
    def __init__(self) -> None:
        super().__init__()
        self.message.update(
            {
                "testing": "Testing using english language."
            }
        )