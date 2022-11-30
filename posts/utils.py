from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from users.utils import paginated_response
from .models import Post
from .serializers import PostCreateSerializer, PostSerializer


@paginated_response(PostSerializer)
def get_all_posts(request: Request):
    """Retrieve all users."""
    return Post.objects.all() 


def create_post(request: Request):
    """Create new post."""
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        post = Post(**serializer.data)
        post.author = request.user
        post.save()
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_post_object(pk: int):
    """Retrieve post object by id."""
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404


def get_post_by_id(request: Request, pk: int):
    """Retrieve post object by id and send response."""
    post = get_post_object(pk)

    serializer = PostSerializer(post)
    return Response(serializer.data)


def update_post(request: Request, pk: int):
    """Update post."""
    post = get_post_object(pk)

    if post.author != request.user:
        return Response({'detail': 'This is not your post'}, status=status.HTTP_403_FORBIDDEN)

    serializer = PostCreateSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        post.refresh_from_db()
        return Response(PostSerializer(post).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_post(request: Request, pk: int):
    """Delete post."""
    post = get_post_object(pk)

    if post.author != request.user:
        return Response({'detail': 'This is not your post'}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    