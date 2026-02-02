from typing import Any

class IndonesianBaseMessageTranslator():
    def __init__(self) -> None:
        self.message: dict[str, str] = {
            "success": "Sukses",
            "server_running": "Server sedang berjalan."
        }

    def get(self, key: str):
        return self.message.get(key, f"Missing translation for {key}")
    
    def format(self, key: str, **kwargs: Any) -> str:
        template = self.get(key)
        return template.format(**kwargs)