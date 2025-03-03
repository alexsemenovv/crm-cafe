import logging

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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Dish, Order
from .serializers import OrderSerializer

log = logging.getLogger(__name__)


class OrderViewSet(ModelViewSet):
    """
    Набор представлений для действий над Order
    Полный CRUD для сущностей заказа
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["status"]
    filterset_fields = [
        "table_number",
        "status",
    ]
    ordering_fields = [
        "table_number",
        "total_price",
        "status",
    ]



def order_index(request: HttpRequest) -> HttpResponse:
    """
    Функция возвращает базовый шаблон при обращении к 'orders/'
    :param request: HttpRequest - запрос
    :return: HttpResponse - шаблон в формате html
    """
    log.debug("Rendering order index")
    return render(
        request,
        'ordersapp/base.html'
    )


class DishCreateView(CreateView):
    """
    Класс для создания блюда
    """
    log.debug("Create new dish")
    model = Dish
    fields = "name", "description", "price"
    success_url = reverse_lazy(
        "ordersapp:dishes_list"
    )


class DishListView(ListView):
    """
    Класс для отображения списка блюд
    """
    log.debug("Dishes list")
    template_name = "ordersapp/dishes_list.html"
    context_object_name = "dishes"
    queryset = Dish.objects.all()


class OrderCreateView(CreateView):
    """
    Класс для создания заказа
    """
    log.debug("Create order")
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
    log.debug("Orders list")
    template_name = "ordersapp/orders_list.html"
    context_object_name = "orders"
    queryset = Order.objects.all()


class OrderDeleteView(DeleteView):
    """
    Класс для получения деталей продукта
    """
    log.debug("Order details")
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")


class OrderUpdateView(UpdateView):
    """
    Класс для обновления статуса заказа
    """
    log.debug("Update status order")
    model = Order
    fields = ("status", "items")
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("ordersapp:orders_list")


class OrderSearchListView(ListView):
    """
    Класс для поиска заказа по номеру стола,
    либо статусу заказа
    """
    log.debug("Search order by status or table number")
    model = Order
    template_name = "ordersapp/order_search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Order.objects.filter(
            Q(status__icontains=query) | Q(table_number__icontains=query)
        )
        return object_list


class OrderTotalIncomesListView(ListView):
    """
    Класс для подсчета выручки за смену
    """
    log.debug("Total incomes order")
    model = Order
    template_name = "ordersapp/total_incomes.html"

    def get_queryset(self):
        orders = Order.objects.prefetch_related("items").filter(
            status__contains="Оплачено"
        )
        total = sum((item.total_price for item in orders.all()))
        return orders, total
