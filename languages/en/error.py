from languages.en.base import EnglishBaseMessageTranslator


class EnglishErrorMessageTranslator(EnglishBaseMessageTranslator):
    def __init__(self) -> None:
        super().__init__()
        self.message.update(
            {
                "validation_error": "Invalid input. Please check your request data.",
                "data_not_found_error": "Data not found.",
            }
        )