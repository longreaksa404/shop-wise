from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_seller
        )

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_buyer
        )

class IsAdminOrSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin or request.user.is_seller)
        )

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj): # obj is the actual database record
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin or obj == request.user)
        )