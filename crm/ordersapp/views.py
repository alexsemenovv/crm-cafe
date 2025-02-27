from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Dish


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


class DishCreateView(CreateView):
    """
    Класс для создания блюда
    """
    model = Dish
    fields = "name", "description", "price"

    success_url = reverse_lazy(
        "ordersapp:index"
    )

class DishListView(ListView):
    """
    Класс для отображения списка блюд
    """
    template_name = "ordersapp/dishes_list.html"
    context_object_name = "dishes"
    queryset = Dish.objects.all()


