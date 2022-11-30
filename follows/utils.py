from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from users.utils import paginated_response
from users.serializers import UserSerializer

User = get_user_model()


def get_user_object(pk: int):
    """Retrieve user object or raise 404 error."""
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404


def follow_user(request: Request, pk: int):
    """Follow user."""
    user = get_user_object(pk)
    current_user = request.user

    if not current_user.is_following(user):
        current_user.follow(user)
        return Response(status=status.HTTP_201_CREATED)
    return Response({'detail': 'You already follow this user.'}, status=status.HTTP_404_NOT_FOUND)


def unfollow_user(request: Request, pk: int):
    """Unfollow user."""
    user = get_user_object(pk) 
    current_user = request.user

    if current_user.is_following(user):
        current_user.unfollow(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'detail': "You don't follow this user."}, status=status.HTTP_404_NOT_FOUND)


def is_following(request: Request, pk: int):
    """Check if user is followed by current user."""
    user = get_user_object(pk)
    current_user = request.user

    if not current_user.is_following(user):
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


@paginated_response(UserSerializer)
def retrieve_following(request: Request):
    """Retrieve users current user is following."""
    current_user = request.user 
    return User.objects.filter(followers=current_user).all()


@paginated_response(UserSerializer)
def retrieve_followers(request: Request):
    """Retrieve current user followers."""
    current_user = request.user 
    return User.objects.filter(following=current_user).all()


@paginated_response(UserSerializer)
def get_user_following(request: Request, pk: int):
    """Retrieve users user is following."""
    user = get_user_object(pk)
    return User.objects.filter(followers=user).all() 


@paginated_response(UserSerializer)
def get_user_followers(request: Request, pk: int):
    """Retrieve user followers."""
    user = get_user_object(pk)
    return User.objects.filter(following=user).all()
    