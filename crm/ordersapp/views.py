from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    UpdateView,
)

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

    success_url = reverse_lazy(
        "ordersapp:orders_list"
    )


class OrderListView(ListView):
    """
    Класс для отображения списка заказов
    """
    template_name = "ordersapp/orders_list.html"
    context_object_name = "orders"
    queryset = Order.objects.all()


class OrderDeleteView(DeleteView):
    """
    Класс для получения деталей продукта
    """
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")


class OrderUpdateView(UpdateView):
    """
    Класс для обновления статуса заказа
    """
    model = Order
    fields = ("status",)
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("ordersapp:orders_list")


class OrderSearchListView(ListView):
    """
    Класс для поиска заказа по номеру стола,
    либо статусу заказа
    """
    model = Order
    template_name = "ordersapp/order_search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Order.objects.filter(
            Q(status__icontains=query) | Q(table_number__icontains=query)
        )
        return object_list
