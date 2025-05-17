from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return JsonResponse({"message": "Welcome to the index page of metlims"})

def test_api(request):
    return JsonResponse({"message": "Hello from the test API its working this is coming from the main app"})


# Create your views here.
