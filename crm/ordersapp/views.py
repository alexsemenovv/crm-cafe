from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.

def order_index(request: HttpRequest) -> HttpResponse:
    """
    Функция возвращает базовый шаблон при обращении к 'orders/'
    :param request: HttpRequest - запрос
    :return: HttpResponse - шаблон в формате html
    """
    return render(
        request,
        'ordersapp/base.html'
    )
