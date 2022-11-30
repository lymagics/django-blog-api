from hashlib import md5
from datetime import datetime, timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Django model to represent 'users' table."""
    about_me = models.CharField(max_length=128, default='')
    last_seen = models.DateTimeField(auto_now_add=True)
    member_since = models.DateTimeField(auto_now_add=True)
    following = models.ManyToManyField('CustomUser', blank=True, related_name='followers')

    @property
    def avatar_url(self):
        """Get user avatar url."""
        hash = md5(self.email.encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{hash}'

    def ping(self):
        """Update users last seen."""
        self.last_seen = datetime.now(tz=timezone.utc)
        self.save()

    def is_following(self, user: 'CustomUser'):
        """Check if user is followed by current user."""
        return user in self.following.all()

    def is_followed_by(self, user: "CustomUser"):
        """Check if user is current user follower."""
        return user in self.followers.all()

    def follow(self, user: 'CustomUser'):
        """Follow user."""
        self.following.add(user) 

    def unfollow(self, user: 'CustomUser'):
        """Unfollow user."""
        self.following.remove(user) 

    def __str__(self):
        return self.username
