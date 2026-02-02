from pydantic import BaseModel
from typing import Optional, Any
from languages.translator import get_translator
from languages.context import current_lang


resolved_lang = current_lang.get()
translator = get_translator(resolved_lang)


class Default(BaseModel):
    message: str = translator.get("success")
    data: Optional[dict[str, Any]] = None