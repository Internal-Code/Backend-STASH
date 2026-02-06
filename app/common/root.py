from litestar import get, status_codes
from schemas.response import Default
from languages.translator import get_translator
from languages.context import current_lang

@get(status_code=status_codes.HTTP_200_OK, summary="Root endpoint.", tags=["Root"], response=Default)
async def root() -> Default:
    response = Default()
    resolved_lang = current_lang.get()
    translator = get_translator(resolved_lang)
    response.message = translator.get("server_running")
    return response