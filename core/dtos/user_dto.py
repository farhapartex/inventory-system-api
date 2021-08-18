from pydantic import BaseModel, validator, Field
from typing import Optional
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError


class UserRegistrationDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @validator('email')
    def email_validator(cls, email):
        try:
            email_validator = EmailValidator()
            email_validator(email)
        except DjangoValidationError as error:
            raise ValueError('Please enter a valid email')
        return email

    @validator('first_name')
    def first_name_validator(cls, first_name):
        if len(first_name) == 0:
            raise ValueError('Please enter a valid first name')
        return first_name

    @validator('last_name')
    def last_name_validator(cls, last_name):
        if len(last_name) == 0:
            raise ValueError('Please enter a valid last name')
        return last_name

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 6:
            raise ValueError('Your password length should be more then 6')
        return password


class UserDTO(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    username: str
    email: str
    role: str
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    is_active: Optional[bool] = False
    is_staff: Optional[bool] = False


class UserMinimalDTO(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    username: str
    email: str


class UserRegistrationSuccessDTO(BaseModel):
    user: Optional[UserDTO] = None
    success: bool = False
    message: str


class AccountVerifyDTO(BaseModel):
    email: str
    code: str

    @validator('email')
    def email_validator(cls, email):
        try:
            email_validator = EmailValidator()
            email_validator(email)
        except DjangoValidationError as error:
            raise ValueError('Please enter a valid email')
        return email

    @validator('code')
    def code_validator(cls, code):
        if len(code) < 0:
            raise ValueError('Please enter a valid code')
        return code


class AccountVerifySuccessDTO(BaseModel):
    message: str
    success: bool = True

