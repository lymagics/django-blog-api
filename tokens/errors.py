from rest_framework import status
from rest_framework.response import Response


def unauthorized():
    """HTTP 401 Unauthorized error."""
    return Response({'message': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    