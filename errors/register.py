from typing import Any
from litestar import status_codes, MediaType, Request, Response

class RegisterCustomerror():
    def handler(self, _: Request[Any, Any, Any], exc: Exception) -> Response[dict[str, Any]]:
        status_code = getattr(exc, "status_code", status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        message = getattr(exc, "detail", str(exc))
        errors = getattr(exc, "errors", {})
        print(errors)

        return Response(
            content={
                "message": message,
                "errors": errors,
            },
            status_code=status_code,
            media_type=MediaType.JSON,
        )