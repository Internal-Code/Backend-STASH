from languages.id.base import IndonesianBaseMessageTranslator


class IndonesianErrorMessageTranslator(IndonesianBaseMessageTranslator):
    def __init__(self) -> None:
        super().__init__()
        self.message.update(
            {
                "validation_error": "Input tidak valid. Silakan periksa data permintaan Anda.",
                "data_not_found_error": "Data tidak ditemukan.",
            }
        )