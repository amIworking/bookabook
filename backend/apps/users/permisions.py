from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrAdminUser(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):

        return bool(request.method in SAFE_METHODS
                    or obj == request.user
                     or request.user.is_staff == True)

class NotAllowedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'message': "You're not allowed"}
    default_code = 'not_allowed'

class AnyNotAllowed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        raise NotAllowedException()