from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from tokens.authentication import CustomTokenAuthentication, CustomTokenAuthenticationScheme
from .serializers import PaginationQuerySerializer, PostPaginationSerializer, PostCreateSerializer, PostSerializer
from .utils import create_post, delete_post, get_all_posts, get_post_by_id, update_post


class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [CustomTokenAuthentication]

    @extend_schema(
        summary='Retrieve all posts', parameters=[PaginationQuerySerializer],
        responses=PostPaginationSerializer, tags=['Posts'], auth=[])
    def get(self, request: Request):
        """Retrieve all posts."""
        return get_all_posts(request) 

    @extend_schema(
        summary='Create new post', request=PostCreateSerializer,
        responses=PostSerializer, tags=['Posts'],
        parameters=[CustomTokenAuthenticationScheme])
    def post(self, request: Request):
        """Create new post."""
        return create_post(request) 


class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [CustomTokenAuthentication]

    @extend_schema(
        summary='Retrieve post by id', responses=PostSerializer,
        tags=['Posts'], auth=[])
    def get(self, request: Request, pk: int):
        """Retrieve post by id."""
        return get_post_by_id(request, pk) 

    @extend_schema(
        summary='Edit post information', request=PostCreateSerializer,
        responses=PostSerializer, tags=['Posts'], parameters=[CustomTokenAuthenticationScheme])
    def put(self, request: Request, pk: int):
        """Edit post information."""
        return update_post(request, pk) 

    @extend_schema(summary='Delete post', tags=['Posts'], parameters=[CustomTokenAuthenticationScheme])
    def delete(self, request: Request, pk: int):
        """Delete post."""
        return delete_post(request, pk)
