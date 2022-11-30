from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAutenticatedForCreate(BasePermission):
    """Custom permission to allow POST request for only authenticated users."""
    def has_permission(self, request: Request, view):
        """Allow unauthorized access for all methods except POST."""
        if request.method == 'POST':
            return request.user.is_authenticated

        return True
