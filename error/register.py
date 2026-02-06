from typing import Any
from litestar import status_codes, MediaType, Request, Response
from litestar.exceptions import HTTPException
from languages.context import current_lang
from languages.translator import get_translator

class CustomException():
    def handler(self, _: Request[Any, Any, Any], exc: Exception) -> Response[dict[str, Any]]:
        resolved_lang = current_lang.get()
        translator = get_translator(resolved_lang)
        status_code = getattr(exc, "status_code", status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
        error = getattr(exc, "extra", None)
        return Response(
            content={
                "message": translator.get("validation_error"),
                "error": error,
            },
            status_code=status_code,
            media_type=MediaType.JSON,
        )

    def pydantic_handler(self, _: Request[Any, Any, Any], exc: Exception) -> Response[dict[str, Any]]:
        print(exc)
        resolved_lang = current_lang.get()
        translator = get_translator(resolved_lang)

        status_code = getattr(exc, "status_code", status_codes.HTTP_422_UNPROCESSABLE_ENTITY)
        extra = getattr(exc, "extra", None)
        error: dict[str, list[str]] = {}
        print(extra)
        if extra:
            for err in extra:
                key = err.get("key")
                message = err.get("message")

                if key not in error:
                    error[key] = []

                error[key].append(message)

        print(error)

        return Response(
            content={
                "message": translator.get("validation_error"),
                "error": error,
            },
            status_code=status_code,
            media_type=MediaType.JSON,
        )