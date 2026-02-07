from json import JSONDecodeError
from typing import Any
from litestar import status_codes, MediaType, Request, Response
from litestar.exceptions import HTTPException
from pydantic_core import ValidationError
from languages.context import current_lang
from languages.translator import get_translator


class CustomException:
    def base_handler(self, _: Request[Any, Any, Any], exc: HTTPException) -> Response[dict[str, Any]]:
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
    
    def pydantic_handler(
        self,
        _: Request[Any, Any, Any],
        exc: ValidationError
    ) -> Response[dict[str, Any]]:

        resolved_lang = current_lang.get()
        translator = get_translator(resolved_lang)

        errors: dict[str, list[str]] = {}

        for err in exc.errors():
            loc = err.get("loc", [])
            msg = err.get("msg", "Invalid value")
            key = ".".join(str(x) for x in loc) if loc else "non_field_error"
            errors.setdefault(key, []).append(msg)

        return Response(
            content={
                "message": translator.get("validation_error"),
                "error": errors,
            },
            status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
            media_type=MediaType.JSON,
        )
        
    def json_handler(
        self,
        _: Request[Any, Any, Any],
        error: JSONDecodeError
    ) -> Response[dict[str, Any]]:
        resolved_lang = current_lang.get()
        translator = get_translator(resolved_lang)
        return Response(
            content={
                "message": translator.get("validation_error"),
                "error": str(error),
            },
            status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
            media_type=MediaType.JSON,
        )
        
        
        