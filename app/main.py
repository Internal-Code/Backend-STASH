import json
from error.custom import DataNotFoundError
from dataclasses import dataclass
from typing import Optional, Annotated, Union
from litestar import Litestar, post, status_codes, Router, Request
from litestar.params import Body, Parameter
from litestar.datastructures import UploadFile
from pydantic import BaseModel, Field, EmailStr, constr
from schemas.response import Default
from app.common.root import root
from app.docs.scalar import get_scalar_openapi_config
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.enums import RequestEncodingType
from middleware.language import LanguageMiddleware
from middleware.timeout import TimeoutMiddleware
from error.register import CustomException
from error.custom import BaseError
from litestar.exceptions import ValidationException
from litestar.exceptions import HTTPException
from pydantic_core import ValidationError

throttle_config = RateLimitConfig(rate_limit=("second", 10))
custom_exception = CustomException()


class User(BaseModel):
    user: str


class UserConvert(BaseModel):
    name: str = Field(min_length=1)
    age: Optional[int] = Field(ge=1)
    address: str

class Users(BaseModel):
    users: list[UserConvert]

@post(path="/register", status_code=status_codes.HTTP_201_CREATED, response=Default)
async def register_user(
    data: Annotated[User, Body(media_type=RequestEncodingType.MULTI_PART)]
) -> Default:
    try:
        parsed = json.loads(data.user)
        Users(users=parsed)
    except ValidationException:
        raise
    except json.JSONDecodeError:
        raise 
    except ValidationError:
        raise
    response = Default()
    response.message = "testing"
    return response

root_router = Router(
    path="/",
    route_handlers=[root],
    middleware=[throttle_config.middleware]
)

app = Litestar(
    route_handlers=[root_router, register_user],
    openapi_config=get_scalar_openapi_config(),
    middleware=[TimeoutMiddleware(), LanguageMiddleware()],
    exception_handlers={
        ValidationError: custom_exception.pydantic_handler,
        json.JSONDecodeError: custom_exception.json_handler,
        ValidationException: custom_exception.base_handler
    }
)
