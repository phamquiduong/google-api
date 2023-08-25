from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, validator

from core.validator.phone_number_validator import phone_number_validator


class UserBaseSchema(BaseModel):
    email: EmailStr

    # Optional fields
    password_exp: datetime | None = None

    address: str | None = None
    full_name: str | None = None
    phone_number: str | None = None

    google_access_token: str | None = None
    google_refresh_token: str | None = None

    @validator('phone_number')
    @classmethod
    def user_phone_number_validator(cls, phone_number):
        return phone_number_validator(phone_number) if phone_number else None


class UserSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    hashed_password: str


class UserInSchema(UserBaseSchema):
    password: str


class UserOutSchema(UserBaseSchema):
    id: int
    is_active: bool


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
