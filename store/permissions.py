from rest_framework.permissions import BasePermission
from core.enums import RoleEnum


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list":
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy'] and request.user.role == RoleEnum.OWNER.name:
            return True
        else:
            return False

