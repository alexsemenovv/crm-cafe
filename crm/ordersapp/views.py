from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def order_index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>Hello world!</h1>')