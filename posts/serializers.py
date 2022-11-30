from rest_framework import serializers

from users.serializers import UserSerializer, PaginationQuerySerializer
from .models import Post


class PostCreateSerializer(serializers.Serializer):
    """DRF serializer for post model creation data validation."""
    title = serializers.CharField(max_length=50)
    content = serializers.CharField() 

    def update(self, instance: Post, validated_data: dict):
        """This method will be called during post update in serializer.save()."""
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        instance.save()
        return instance
     

class PostSerializer(serializers.Serializer):
    """DRF serializer for post model."""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    content = serializers.CharField() 
    created_at = serializers.DateTimeField(read_only=True)
    author = UserSerializer()


class PostPaginationSerializer(PaginationQuerySerializer):
    data = PostSerializer(many=True)
    