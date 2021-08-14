from pydantic import BaseModel, validator
from django.core.validators import EmailValidator


class UserRegistrationDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @validator('email')
    def email_validator(cls, email):
        email_validator = EmailValidator()
        email_validator(email)
        return email


class UserDTO(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    is_stuff: bool
