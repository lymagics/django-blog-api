import secrets
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Token(models.Model):
    """Django ORM model to represent 'tokens' table."""
    access_token = models.CharField(max_length=64, db_index=True)
    access_expiration = models.DateTimeField()
    refresh_token = models.CharField(max_length=64, db_index=True)
    refresh_expiration = models.DateTimeField()

    user = models.ForeignKey(User, related_name='tokens', on_delete=models.CASCADE)

    def generate(self):
        """Generate token pair."""
        self.access_token = secrets.token_urlsafe()
        self.access_expiration = datetime.utcnow() + \
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token = secrets.token_urlsafe()
        self.refresh_expiration = datetime.utcnow() + \
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    def expire(self):
        """Expire token pair."""
        self.access_expiration = datetime.utcnow()
        self.refresh_expiration = datetime.utcnow()

    @staticmethod
    def clean():
        """Clean tokens that expired for more than a day."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        Token.objects.filter(refresh_expiration__lt=yesterday).delete()

    def __str__(self):
        return f'{self.user.username} token'    
