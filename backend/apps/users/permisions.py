from rest_framework.exceptions import APIException

from rest_framework.permissions import SAFE_METHODS, BasePermission

from rest_framework.status import HTTP_403_FORBIDDEN

from apps.users.models import User


class IsOwnerOrAdminUser(BasePermission):

    def has_object_permission(self, request, view, obj):

        return bool(
                    request.method in SAFE_METHODS
                    or obj == request.user
                    or request.user.is_staff == True
                   )


class NotAllowedException(APIException):

    status_code = HTTP_403_FORBIDDEN
    default_detail = {'message': "You're not allowed"}
    default_code = 'not_allowed'


class AnyNotAllowed(BasePermission):

    def has_object_permission(self, request, view, obj):
        raise NotAllowedException()


class IsRegistered(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.id is not None)
