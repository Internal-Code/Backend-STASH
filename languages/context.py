from contextvars import ContextVar

current_lang: ContextVar[str] = ContextVar("lang", default="en")