from rest_framework import permissions

from core.enums.roles import RoleEnum


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.OWNER.name


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.ADMIN.name


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.CUSTOMER.name

