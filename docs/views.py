from django.shortcuts import render
from django.http import HttpRequest


def elements_ui(request: HttpRequest):
    """Element UI documentation."""
    return render(request, 'elements.html')


def swagger_ui(request: HttpRequest):
    """Swagger UI documentation."""
    return render(request, 'swagger-ui.html')


def rapidoc_ui(request: HttpRequest):
    """Rapidoc UI documentation."""
    return render(request, 'rapidoc.html')


def redoc_ui(request: HttpRequest):
    """Redoc UI documentation."""
    return render(request, 'redoc.html')
