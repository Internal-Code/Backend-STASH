from pydantic import BaseModel, Field, EmailStr

class RegisterUserPayload(BaseModel):
    email: EmailStr = Field(description="User email.")
    pin: int = Field(description="User PIN.", max_digits=6, min_length=6)