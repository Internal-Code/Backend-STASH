from typing import Any

class EnglishBaseMessageTranslator():
    def __init__(self) -> None:
        self.message: dict[str, str] = {
            "success": "Success",
            "server_running": "Server running.",
        }

    def get(self, key: str):
        return self.message.get(key, f"Missing translation for {key}")
    
    def format(self, key: str, **kwargs: Any) -> str:
        template = self.get(key)
        return template.format(**kwargs)