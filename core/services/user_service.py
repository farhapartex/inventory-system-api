from random import randint

from django.db.models import Q
from django.db import transaction
from django.http import HttpRequest
from pydantic.error_wrappers import ValidationError
from core.dtos import UserRegistrationDTO, UserDTO, UserRegistrationSuccessDTO, AccountVerifyDTO, \
    AccountVerifySuccessDTO
from core.enums.roles import RoleEnum
from core.exceptions import UserExistsException, UserNotFoundException, UserAlreadyActiveException
from core.models import User, UserAuthCode
from store.signals import trigger_create_employee


class UserService:
    @classmethod
    def _generate_random_number(cls, n: int) -> str:
        return ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])

    @classmethod
    def _get_user_auth_code(cls, user: User, auth_code_dto: AccountVerifyDTO) -> UserAuthCode:
        user_auth_code: UserAuthCode = UserAuthCode.objects.filter(user=user, code=auth_code_dto.code, is_used=False).first()
        return user_auth_code

    @classmethod
    def _get_user_by_email_username(cls, identifier: str) -> User:
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        return user

    @classmethod
    def _create_user(cls, data: dict) -> User:
        with transaction.atomic():
            user = User.objects.create(**data)
            user.save()
            UserAuthCode.objects.create(user=user, code=cls._generate_random_number(6))
            return user

    @classmethod
    def create_user(cls, request: HttpRequest, request_data: UserRegistrationDTO) -> UserRegistrationSuccessDTO:
        instance = cls._get_user_by_email_username(request_data.email)
        if instance:
            raise UserExistsException("User already in system.")

        data = {
            "first_name": request_data.first_name,
            "last_name": request_data.last_name,
            "username": request_data.email,
            "email": request_data.email,
            "role": request_data.role,
            "is_active": False
        }

        user = cls._create_user(data)
        user.set_password(request_data.password)
        user.save()

        if request.user.role == RoleEnum.OWNER.name:
            trigger_create_employee.send(sender=user.__class__, request=request, employee=user, store=request.user.store)

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
            message="Account registration is completed successfully."
        )

    @classmethod
    def verify_user_account(cls, request_data: AccountVerifyDTO) -> AccountVerifySuccessDTO:
        instance: User = cls._get_user_by_email_username(request_data.email)
        if instance is None:
            raise UserNotFoundException("User already in system.")
        if instance.is_active and instance.is_verified:
            raise UserAlreadyActiveException("User already active and verified")

        user_auth_code: UserAuthCode = cls._get_user_auth_code(user=instance, auth_code_dto=request_data)
        if user_auth_code is None:
            raise UserAlreadyActiveException("User already active")

        user_auth_code.is_used = True
        user_auth_code.save()

        instance.is_verified = True
        instance.is_active = True
        instance.save()

        return AccountVerifySuccessDTO(message="User account verified successfully.")
