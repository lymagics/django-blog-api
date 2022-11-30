from django.urls import path 
from . import views

urlpatterns = [
    path('me/', views.CurrentUserDetail.as_view(), name='current-user-detail'),
    path('<username>/', views.UserDetail.as_view(), name='user-detail'),
    path('<username>/posts/', views.UserPostList.as_view(), name='user-post-list'),
    path('', views.UserList.as_view(), name='user-list'),
]