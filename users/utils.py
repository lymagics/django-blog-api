from functools import wraps

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from posts.serializers import PostSerializer
from posts.models import Post
from .serializers import UserSerializer

User = get_user_model()


def paginated_response(serializer_class):
    """If you decorate function with this, it will ensure paginated response."""
    def wrapper(f):
        @wraps(f)
        def paginate(request: Request, *args, **kwargs):
            limit = int(request.query_params.get('limit', 10))
            offset = int(request.query_params.get('offset', 0))

            query = f(request, *args, **kwargs)
            pagination_query = query[offset:limit]
            serializer = serializer_class(pagination_query, many=True)

            data = {
                'limit': limit,
                'offset': offset,
                'data': serializer.data
            }

            return Response(data)
        return paginate
    return wrapper


@paginated_response(UserSerializer)
def get_all_users(request: Request):
    """Retrieve all users."""
    return User.objects.all()


def create_user(request: Request):
    """Create new user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user_object(username: str):
    """Retrieve user by username."""
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404


def get_user_by_username(request: Request, username: str):
    """Retrieve user by username and send response."""
    user = get_user_object(username)
    serializer = UserSerializer(user)
    return Response(serializer.data)


def update_user(request: Request):
    """Update user informstion."""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@paginated_response(PostSerializer)
def get_all_user_posts(request: Request, username: str):
    """Retrieve all user posts."""
    user = get_user_object(username)
    return Post.objects.filter(author=user)
