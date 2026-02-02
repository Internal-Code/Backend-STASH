from litestar import Router, Litestar
from app.common.root import root
from app.docs.scalar import get_scalar_openapi_config
from litestar.middleware.rate_limit import RateLimitConfig
from middlewares.language import LanguageMiddleware
from middlewares.timeout import TimeoutMiddleware
from errors.register import RegisterCustomerror
from errors.custom import BaseError

throttle_config = RateLimitConfig(rate_limit=("second", 10))
register_custom_error = RegisterCustomerror()


root_router = Router(
    path="/",
    route_handlers=[root],
    middleware=[throttle_config.middleware]
)

app = Litestar(
    route_handlers=[root_router],
    openapi_config=get_scalar_openapi_config(),
    middleware=[TimeoutMiddleware(), LanguageMiddleware()],
    exception_handlers={BaseError: register_custom_error.handler}
)
