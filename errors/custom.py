from typing import Optional, Any
from litestar import status_codes
from litestar.exceptions import HTTPException
from languages.context import current_lang
from languages.translator import get_translator


class BaseError(HTTPException):
    """Base exception for all custom application errors."""

    def __init__(
        self,
        status_code: int,
        message_key: str,
        errors: Optional[dict[str, Any]] = None,
        message: Optional[str] = None,
    ) -> None:
        self.current_lang = current_lang.get()
        self.translator = get_translator(self.current_lang)
        self.status_code = status_code
        self.errors = errors or {}
        self.message = message or self.translator.get(message_key)
        super().__init__(self.message)


class DataValidationError(BaseError):
    """Raised when validation of input data fails."""

    def __init__(
        self,
        errors: Optional[dict[str, Any]] = None,
        message: Optional[str] = None,
        message_key: str = "validation_error",
    ):
        super().__init__(
            status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
            message_key=message_key,
            message=message,
            errors=errors,
        )


class DataNotFoundError(BaseError):
    """Raised when requested data is not found."""

    def __init__(
        self,
        errors: Optional[dict[str, Any]] = None,
        message: Optional[str] = None,
        message_key: str = "data_not_found_error",
    ):
        super().__init__(
            status_code=status_codes.HTTP_404_NOT_FOUND,
            message_key=message_key,
            message=message,
            errors=errors,
        )
