from litestar.middleware import ASGIMiddleware
from litestar.types import ASGIApp, Receive, Scope, Send
from litestar import Request
from languages.context import current_lang


class LanguageMiddleware(ASGIMiddleware):
    async def handle(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
        next_app: ASGIApp,
    ) -> None:
        request = Request(scope, receive=receive, send=send) # type: ignore
        language = request.headers.get("accept-language", "en")
        token = current_lang.set(language)
        try:
            await next_app(scope, receive, send)
        finally:
            current_lang.reset(token)
