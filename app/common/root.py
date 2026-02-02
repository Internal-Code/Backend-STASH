from litestar import get
from schemas.response import Default
from languages.translator import get_translator
from languages.context import current_lang
from errors.custom import DataNotFoundError

@get(status_code=200, summary="Root endpoint.", tags=["Root"], response=Default)
async def root() -> Default:
    raise DataNotFoundError(errors={"test":"test"})
    response = Default()
    resolved_lang = current_lang.get()
    translator = get_translator(resolved_lang)
    response.message = translator.get("server_running")
    return response