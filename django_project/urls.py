from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularJSONAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tokens/', include('tokens.urls')),
    path('posts/', include('posts.urls')),
    path('schema/', SpectacularJSONAPIView.as_view(), name='schema'),
    path('docs/', include('docs.urls')),
    path('', include('follows.urls')),
]
