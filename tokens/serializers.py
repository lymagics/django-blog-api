from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """DRF serializer for token model."""
    access_token = serializers.CharField(max_length=64)
    refresh_token = serializers.CharField(max_length=64, required=False)
