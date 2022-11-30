from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.authentication import BasicAuthentication

from .utils import create_token, refresh_token, revoke_token
from .permissions import IsAutenticatedForCreate
from .serializers import TokenSerializer


class TokenView(APIView):
    permission_classes = [IsAutenticatedForCreate]
    authentication_classes = [BasicAuthentication]

    @extend_schema(summary='Create new access token', tags=['Tokens'])
    def post(self, request: Request):
        """Create new access token."""
        return create_token(request) 

    @extend_schema(
        summary='Refresh token', request=TokenSerializer,
        responses=TokenSerializer, tags=['Tokens'], auth=[])
    def put(self, request: Request):
        """Refresh token."""
        return refresh_token(request) 

    @extend_schema(
        summary='Revoke access token', request=TokenSerializer,
        tags=['Tokens'], auth=[])
    def delete(self, request: Request):
        """Revoke access token."""
        return revoke_token(request) 
