from datetime import datetime, timezone

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .errors import unauthorized
from .models import Token 


def create_token(request: Request):
    """Create token pair."""
    token = Token(user=request.user)
    token.generate()
    token.save()

    Token.clean()

    return token_response(token)


def refresh_token(request: Request):
    """Refresh expired token."""
    refresh_token = get_refresh_token(request)
    if not refresh_token:
        return unauthorized()

    token = verify_token(refresh_token)
    if token is None:
        return unauthorized()

    token.expire()
    new_token = Token(user=token.user)
    new_token.generate()
    new_token.save()

    return token_response(new_token)


def revoke_token(request: Request):
    """Revoke token."""
    refresh_token = get_refresh_token(request)
    if not refresh_token:
        return unauthorized()

    token = verify_token(refresh_token)
    if token is None:
        return unauthorized()

    token.expire()
    token.save()

    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('refresh_token')
    return response


def token_response(token: Token):
    """Prepair data for token response."""
    data = {
        'access_token': token.access_token,
        'refresh_token': token.refresh_token
        if settings.REFRESH_TOKEN_IN_BODY else ''
    }

    response = Response(data, status=status.HTTP_201_CREATED)

    if settings.REFRESH_TOKEN_IN_COOKIE:
        response.set_cookie(
            'refresh_token', token.refresh_token,
            httponly=True, secure=not settings.DEBUG
        )

    return response


def get_refresh_token(request: Request):
    """Retrieve refresh token from cookie or request body."""
    return request.COOKIES.get('refresh_token') or request.data.get('refresh_token')


def verify_token(token: str):
    """Verify if token is valid."""
    token = Token.objects.filter(refresh_token=token).first()
    if token is not None and token.refresh_expiration > datetime.now(tz=timezone.utc):
        return token 
