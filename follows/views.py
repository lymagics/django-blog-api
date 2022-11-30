from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from tokens.authentication import CustomTokenAuthentication, CustomTokenAuthenticationScheme
from users.serializers import PaginationQuerySerializer, UserPaginationSerializer
from .utils import follow_user, unfollow_user, is_following, retrieve_following, retrieve_followers, \
    get_user_followers, get_user_following


class FollowingList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    @extend_schema(
        summary='Retrieve authenticated user following', parameters=[PaginationQuerySerializer],
        responses=UserPaginationSerializer, tags=['Follow'])
    def get(self, request: Request):
        """Retrieve authenticated user following."""
        return retrieve_following(request) 


class FollowingDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    @extend_schema(summary='Check if current user follows this user', tags=['Follow'])
    def get(self, request: Request, pk: int):
        """Check if current user follows this user."""
        return is_following(request, pk)

    @extend_schema(summary='Follow user', tags=['Follow'], parameters=[CustomTokenAuthenticationScheme])
    def post(self, request: Request, pk: int):
        """Follow user."""
        return follow_user(request, pk)

    @extend_schema(summary='Unfollow user', tags=['Follow'], parameters=[CustomTokenAuthenticationScheme])
    def delete(self, request: Request, pk: int):
        """Unfollow user."""
        return unfollow_user(request, pk)


class FollowersList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    @extend_schema(
        summary='Retrieve authenticated user followers', 
        parameters=[PaginationQuerySerializer, CustomTokenAuthenticationScheme],
        responses=UserPaginationSerializer, tags=['Follow'])
    def get(self, request: Request):
        """Retrieve authenticated user followers."""
        return retrieve_followers(request) 


@extend_schema(
    summary='Retrieve user following', parameters=[PaginationQuerySerializer],
    responses=UserPaginationSerializer, tags=['Follow'], auth=[])
@api_view(['GET'])
def retrieve_user_following(request: Request, pk: int):
    """Retrieve user following."""
    return get_user_following(request, pk) 


@extend_schema(
    summary='Retrieve user followers', parameters=[PaginationQuerySerializer],
    responses=UserPaginationSerializer, tags=['Follow'], auth=[])
@api_view(['GET'])
def retrieve_user_followers(request: Request, pk: int):
    """Retrieve user followers."""
    return get_user_followers(request, pk) 
