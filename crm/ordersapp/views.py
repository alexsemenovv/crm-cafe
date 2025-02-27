from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Dish, Order


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
        "ordersapp:dishes_list"
    )


class DishListView(ListView):
    """
    Класс для отображения списка блюд
    """
    template_name = "ordersapp/dishes_list.html"
    context_object_name = "dishes"
    queryset = Dish.objects.all()


class OrderCreateView(CreateView):
    """
    Класс для создания заказа
    """
    model = Order
    fields = "table_number", "items"
    template_name_suffix = "_create"

    # TODO изменить перенаправление на order_list
    success_url = reverse_lazy(
        "ordersapp:index"
    )


class OrderListView(ListView):
    """
    Класс для отображения списка заказов
    """
    template_name = "ordersapp/orders_list.html"
    context_object_name = "orders"
    queryset = Order.objects.all()
