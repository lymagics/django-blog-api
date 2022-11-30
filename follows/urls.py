from django.urls import path 
from . import views

urlpatterns = [
    path('me/following/<int:pk>/', views.FollowingDetail.as_view(), name='following-detail'),
    path('me/following/', views.FollowingList.as_view(), name='following-list'),
    path('me/followers/', views.FollowersList.as_view(), name='followers-list'),
    path('users/<int:pk>/following/', views.retrieve_user_following),
    path('users/<int:pk>/followers/', views.retrieve_user_followers),
]