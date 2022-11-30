from typing import Optional
from datetime import datetime, timezone

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed

from .models import Token

User = get_user_model()


def parse_token_header(token_header: str) -> str:
    """Parse HTTP Authorization headers."""
    if token_header.startswith('Bearer '):
        return token_header.split(' ')[1]


def verify_token(token: str) -> Optional[User]:
    """Verify is access token is valid."""
    token = Token.objects.filter(access_token=token).first()
    if token is not None and token.access_expiration > datetime.now(tz=timezone.utc):
        return token.user 


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        """Authenticated user with access token."""
        token_header = request.META.get('HTTP_AUTHORIZATION')
        
        if token_header is not None:
            token = parse_token_header(token_header)
            if token is not None:
                user = verify_token(token)

                if user is not None:
                    user.ping()
                    return (user, None)
            raise AuthenticationFailed('Invalid credentials')
        
        return None


class CustomTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = CustomTokenAuthentication
    name = 'Bearer'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'name': 'Token'
        }
