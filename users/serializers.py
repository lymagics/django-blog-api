from rest_framework import serializers, validators
from .models import CustomUser


class UserSerializer(serializers.Serializer):
    """DRF serializer for user model."""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, validators=[validators.UniqueValidator(CustomUser.objects.all())])
    email = serializers.EmailField(required=True, write_only=True, validators=[validators.UniqueValidator(CustomUser.objects.all())])
    about_me = serializers.CharField(max_length=128, required=False)
    last_seen = serializers.DateTimeField(read_only=True)
    member_since = serializers.DateTimeField(read_only=True)
    avatar_url = serializers.ReadOnlyField()
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def create(self, validated_data):
        """This method will be called during user creation in serializer.save()."""
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        return user

    def update(self, instance: CustomUser, validated_data: dict):
        """This method will be called during user update in serializer.save()."""
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                if attr == 'password':
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)
        instance.save()
        return instance


class PaginationQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10)
    offset = serializers.IntegerField(default=0)


class UserPaginationSerializer(PaginationQuerySerializer):
    data = UserSerializer(many=True)
