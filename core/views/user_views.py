from rest_framework import views, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pydantic.error_wrappers import ValidationError
from core.dtos import UserRegistrationDTO, UserRegistrationSuccessDTO, AccountVerifyDTO, AccountVerifySuccessDTO
from core.dtos.error_dto import ErrorDTO
from core.enums.roles import RoleEnum
from core.exceptions import UserExistsException, UserNotFoundException, UserAlreadyActiveException
from core.permissions import IsOwner, IsAdmin
from core.services import UserService
import logging


logger = logging.getLogger(__name__)


class UserRegistrationView(views.APIView):
    def post(self, request) -> Response:
        data = request.data
        try:
            data['role'] = RoleEnum.OWNER.name
            registration_dto = UserRegistrationDTO.parse_obj(data)
            response: UserRegistrationSuccessDTO = UserService.create_user(registration_dto)
        except ValidationError as error:
            return Response(error.errors(), status=status.HTTP_400_BAD_REQUEST)
        except UserExistsException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details)
            return Response(error_dto.dict(), status=status.HTTP_400_BAD_REQUEST)

        return Response(response.dict(), status=status.HTTP_200_OK)


class VerifyUserAccountView(views.APIView):
    def post(self, request):
        data = request.data
        try:
            acc_verify_dto = AccountVerifyDTO.parse_obj(data)
            response: AccountVerifySuccessDTO = UserService.verify_user_account(request_data=acc_verify_dto)
        except (UserNotFoundException, UserAlreadyActiveException) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details)
            return Response(error_dto.dict(), status=status.HTTP_400_BAD_REQUEST)

        return Response(response.dict(), status=status.HTTP_200_OK)


class CreateStoreUserAPIView(views.APIView):
    permission_classes = (IsAuthenticated, IsOwner, )

    def post(self, request):
        try:
            data = request.data
            registration_dto = UserRegistrationDTO.parse_obj(data)
            response: UserRegistrationSuccessDTO = UserService.create_user(registration_dto)
        except ValidationError as error:
            return Response(error.errors(), status=status.HTTP_400_BAD_REQUEST)
        except UserExistsException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details)
            return Response(error_dto.dict(), status=status.HTTP_400_BAD_REQUEST)

        return Response(response.dict(), status=status.HTTP_200_OK)

