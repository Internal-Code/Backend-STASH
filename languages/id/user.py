from languages.id.base import IndonesianBaseMessageTranslator


class IndonesianUserMessageTranslator(IndonesianBaseMessageTranslator):
    def __init__(self) -> None:
        super().__init__()
        self.message.update(
            {
                "testing": "Testing menggunakan bahasa indonesia."
            }
        )