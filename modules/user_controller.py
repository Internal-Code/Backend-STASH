from typing import Annotated
from litestar import post, status_codes, Controller
from litestar.enums import RequestEncodingType
from litestar.params import Body
from schemas.response import Default
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class RegisterUserPayload(BaseModel):
    email: EmailStr = Field(description="User email.")
    pin: int = Field(description="User PIN.", max_digits=6, min_length=6)

class EquipmentDetail(BaseModel):
    id: int
    name: str

class Equipment(BaseModel):
    name: str 
    brand: EquipmentDetail
    inventory: Optional[EquipmentDetail] = None



class UserController(Controller):
    @post(
        path="/register",
        status_code=status_codes.HTTP_201_CREATED,
        summary="New user registration account.",
        tags=["User"],
        response=Default
    )
    async def register_user(self) -> Default:
        response = Default()
        response.message = "testing"
        return response

    @post(
        path="/equipment",
        status_code=status_codes.HTTP_201_CREATED,
        summary="Test equipment.",
        tags=["User"],
        response=Default
    )
    async def user(self, schema: Annotated[Equipment, Body(media_type=RequestEncodingType.JSON)]) -> Default:
        print(schema)
        response = Default()
        return response