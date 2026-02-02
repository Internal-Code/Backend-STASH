import asyncio
from litestar.middleware import ASGIMiddleware
from litestar.types import ASGIApp, Receive, Scope, Send
from litestar.exceptions import HTTPException
from litestar import status_codes


class TimeoutMiddleware(ASGIMiddleware):
    def __init__(self, timeout: int = 5) -> None:
        self.timeout = timeout
    async def handle(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
        next_app: ASGIApp,
    ) -> None:
        try:
            await asyncio.wait_for(
                next_app(scope, receive, send),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status_codes.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Request timed out after {self.timeout} seconds",
            )
