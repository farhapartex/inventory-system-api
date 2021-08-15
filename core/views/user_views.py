from rest_framework import views, viewsets, status
from rest_framework.response import Response
from pydantic.error_wrappers import ValidationError
from core.dtos import UserRegistrationDTO, UserRegistrationSuccessDTO
from core.dtos.error_dto import ErrorDTO
from core.exceptions import UserExistsException
from core.services import UserService
import logging


logger = logging.getLogger(__name__)


class UserRegistrationView(views.APIView):
    def post(self, request) -> Response:
        data = request.data
        try:
            registration_dto = UserRegistrationDTO.parse_obj(data)
            response: UserRegistrationSuccessDTO = UserService.register_user_as_customer(registration_dto)
        except ValidationError as error:
            return Response(error.errors(), status=status.HTTP_400_BAD_REQUEST)
        except UserExistsException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details)
            return Response(error_dto.dict(), status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logger.error(str(error))
            return Response(ErrorDTO(details="System found some error").dict(), status=status.HTTP_400_BAD_REQUEST)

        return Response(response.dict(), status=status.HTTP_200_OK)

