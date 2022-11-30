from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from tokens.authentication import CustomTokenAuthentication, CustomTokenAuthenticationScheme
from posts.serializers import PostPaginationSerializer
from .utils import create_user, get_all_users, get_all_user_posts, get_user_by_username, update_user
from .serializers import UserSerializer, UserPaginationSerializer, PaginationQuerySerializer


class UserList(APIView):
    @extend_schema(
        summary='Retrieve all users', tags=['Users'],
        responses=UserPaginationSerializer, auth=[],
        parameters=[PaginationQuerySerializer])
    def get(self, request: Request):
        """Retrieve all users."""
        return get_all_users(request)

    @extend_schema(
        summary='Create new user', tags=['Users'],
        responses=UserSerializer, request=UserSerializer,
        auth=[])
    def post(self, request: Request):
        """Create new user."""
        return create_user(request)


class UserDetail(APIView):
    @extend_schema(
        summary='Retrieve user by username', tags=['Users'],
        responses=UserSerializer, auth=[])
    def get(self, request: Request, username: str):
        """Retrieve user by username."""
        return get_user_by_username(request, username) 


class CurrentUserDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    @extend_schema(
        summary='Retrieve authenticated user', tags=['Users'],
        responses=UserSerializer, parameters=[CustomTokenAuthenticationScheme])
    def get(self, request: Request):
        """Retrieve authenticated user."""
        username = request.user.username
        return get_user_by_username(request, username) 

    @extend_schema(
        summary='Update authenticated user', tags=['Users'],
        request=UserSerializer, responses=UserSerializer, 
        parameters=[CustomTokenAuthenticationScheme])
    def put(self, request: Request):
        """Update authenticated user."""
        return update_user(request) 


class UserPostList(APIView):
    @extend_schema(
        summary='Retrieve all user posts', responses=PostPaginationSerializer,
        parameters=[PaginationQuerySerializer], tags=['Users'], auth=[])
    def get(self, request: Request, username: str):
        """Retrieve all user posts."""
        return get_all_user_posts(request, username) 
