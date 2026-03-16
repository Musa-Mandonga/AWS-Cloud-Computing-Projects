from django.http import HttpResponse
from django.urls import path

def hello_world(request):
    return HttpResponse('Hello, world! This is a Django app running in a container.')

urlpatterns = [
    path('', hello_world),
] 
