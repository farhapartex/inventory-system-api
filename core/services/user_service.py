from django.db.models import Q
from django.db import transaction
from pydantic.error_wrappers import ValidationError
from core.dtos import UserRegistrationDTO, UserDTO, UserRegistrationSuccessDTO
from core.enums.roles import RoleEnum
from core.exceptions import UserExistsException
from core.models import User


class UserService:
    @classmethod
    def get_user_by_email_username(cls, identifier):
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        return user

    @classmethod
    def register_user_as_customer(cls, request_data: UserRegistrationDTO) -> UserRegistrationSuccessDTO:
        instance = cls.get_user_by_email_username(request_data.email)
        if instance:
            raise UserExistsException("User already in system.")

        data = {
            "first_name": request_data.first_name,
            "last_name": request_data.last_name,
            "username": request_data.email,
            "email": request_data.email,
            "role": RoleEnum.CUSTOMER.name,
            "is_active": False
        }

        with transaction.atomic():
            user = User.objects.create(**data)
            user.set_password(request_data.password)
            user.save()

            user_dto = UserDTO(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                role=user.role,
                is_staff=user.is_staff,
                is_superuser=user.is_superuser,
                is_verified=user.is_verified,
                is_active=user.is_active
            )

            return UserRegistrationSuccessDTO(
                user=user_dto,
                success=True,
                message="Your registration is completed successfully."
            )
