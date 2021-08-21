from rest_framework import permissions

from core.enums.roles import RoleEnum


class IS_OWNER(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.OWNER.name