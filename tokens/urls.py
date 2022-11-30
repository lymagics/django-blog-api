from django.urls import path 
from . import views

urlpatterns = [
    path('', views.TokenView.as_view(), name='token-create'),
]