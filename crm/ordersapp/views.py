import logging
from logging import Logger
from typing import Any, List, Tuple, Type

from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Dish, Order
from .serializers import OrderSerializer

log: Logger = logging.getLogger(__name__)


class OrderViewSet(ModelViewSet):
    """
    Набор представлений для действий над Order
    Полный CRUD для сущностей заказа
    Атрибуты:
        - queryset: Запрос для выборки всех заказов из базы данных.
        - serializer_class: Сериализатор для обработки данных модели Order.
        - filter_backends: Набор фильтров (поиск, фильтрация, сортировка).
        - search_fields: Поля, доступные для поиска (по статусу заказа).
        - filterset_fields: Поля, доступные для фильтрации (номер стола, статус).
        - ordering_fields: Поля, доступные для сортировки (номер стола, общая стоимость, статус).
    """

    queryset: QuerySet[Order] = Order.objects.all()
    serializer_class: Type[OrderSerializer] = OrderSerializer
    filter_backends: List[Type] = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields: List[str] = ["status"]
    filterset_fields: List[str] = [
        "table_number",
        "status",
    ]
    ordering_fields: List[str] = [
        "table_number",
        "total_price",
        "status",
    ]

    def list(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        log.debug("Получение списка заказов")
        return super().list(request, *args, **kwargs)

    def create(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        log.info(f"Создание заказа: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        log.info(f"Обновление заказа {kwargs.get('pk')}: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        log.warning(f"Удаление заказа {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)


def order_index(request: HttpRequest) -> HttpResponse:
    """
    Функция возвращает базовый шаблон при обращении к 'orders/'
    :param request: HttpRequest - запрос
    :return: HttpResponse - шаблон в формате html
    """
    log.debug("Rendering order index")
    return render(request, "ordersapp/base.html")


class DishCreateView(CreateView):
    """
    Класс для создания блюда
    """

    log.debug("Create new dish")
    model: Type[Dish] = Dish
    fields: Tuple[str] = "name", "description", "price"
    success_url: str = reverse_lazy("ordersapp:dishes_list")

    def form_valid(self, form: Any):
        log.info(f"Создано новое блюдо: {form.instance.name}")
        return super().form_valid(form)


class DishListView(ListView):
    """
    Класс для отображения списка блюд
    """

    log.debug("Dishes list")
    template_name: str = "ordersapp/dishes_list.html"
    context_object_name: str = "dishes"
    queryset: QuerySet[Dish] = Dish.objects.all()

    def get_queryset(self) -> QuerySet[Dish]:
        log.debug("Запрос списка блюд")
        return super().get_queryset()


class OrderCreateView(CreateView):
    """
    Класс для создания заказа
    """

    log.debug("Create order")
    model: Type[Order] = Order
    fields: Tuple[str, str] = ("table_number", "items")
    template_name_suffix: str = "_create"

    success_url: str = reverse_lazy("ordersapp:orders_list")

    def form_valid(self, form: Any) -> HttpResponse:
        log.info(f"Создан новый заказ: стол {form.instance.table_number}")
        return super().form_valid(form)


class OrderListView(ListView):
    """
    Класс для отображения списка заказов
    """

    log.debug("Orders list")
    template_name: str = "ordersapp/orders_list.html"
    context_object_name: str = "orders"
    queryset: QuerySet[Order] = Order.objects.all()

    def get_queryset(self) -> QuerySet[Order]:
        log.debug("Запрос списка заказов")
        return super().get_queryset()


class OrderDeleteView(DeleteView):
    """
    Класс для удаления заказа
    """

    log.debug("Order details")
    model: Type[Order] = Order
    success_url: str = reverse_lazy("ordersapp:orders_list")

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        log.warning(f"Удаление заказа {kwargs.get('pk')}")
        return super().delete(request, *args, **kwargs)


class OrderUpdateView(UpdateView):
    """
    Класс для обновления статуса заказа
    """

    log.debug("Update status order")
    model: Type[Order] = Order
    fields: Tuple[str, str] = ("status", "items")
    template_name_suffix: str = "_update_form"
    success_url: str = reverse_lazy("ordersapp:orders_list")

    def form_valid(self, form: Any) -> HttpResponse:
        log.info(f"Обновлен заказ {form.instance.pk}: статус {form.instance.status}")
        return super().form_valid(form)


class OrderSearchListView(ListView):
    """
    Класс для поиска заказа по номеру стола,
    либо статусу заказа
    """

    log.debug("Search order by status or table number")
    model: Type[Order] = Order
    template_name: str = "ordersapp/order_search.html"

    def get_queryset(self) -> QuerySet[Order]:
        query: str = self.request.GET.get("q", "")
        log.debug(f"Поиск заказа по запросу: {query}")
        object_list: QuerySet[Order] = Order.objects.filter(
            Q(status__icontains=query) | Q(table_number__icontains=query)
        )
        return object_list


class OrderTotalIncomesListView(ListView):
    """
    Класс для подсчета выручки за смену
    """

    log.debug("Total incomes order")
    model: Type[Order] = Order
    template_name: str = "ordersapp/total_incomes.html"

    def get_queryset(self) -> Tuple[QuerySet[Order], float]:
        orders: QuerySet[Order] = Order.objects.prefetch_related("items").filter(
            status__contains="Оплачено"
        )
        total: float = sum((item.total_price for item in orders.all()))
        log.info(f"Общая выручка за смену: {total}")
        return orders, total
