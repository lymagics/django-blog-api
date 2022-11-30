from django.urls import path 
from . import views

urlpatterns = [
    path('elements/', views.elements_ui, name='elements-ui'),
    path('swagger-ui/', views.swagger_ui, name='swagger-ui'),
    path('rapidoc/', views.rapidoc_ui, name='rapidoc-ui'),
    path('redoc/', views.redoc_ui, name='redoc-ui'),
]