from rest_framework import views, viewsets, status
from rest_framework.response import Response
from core.dtos import UserRegistrationDTO
from core.services import UserService


class UserRegistrationView(views.APIView):
    def post(self, request) -> Response:
        data = request.data
        registration_dto = UserRegistrationDTO.parse_obj(data)
        response = UserService.register_user(registration_dto)
        return Response(response, status=status.HTTP_200_OK)

