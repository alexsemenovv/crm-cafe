from django.urls import path

from .views import (
    order_index,
    DishCreateView,
    DishListView,
    OrderCreateView,
)

app_name = "ordersapp"

urlpatterns = [
    path("", order_index, name="index"),
    path("dishes/create/", DishCreateView.as_view(), name='dish_create'),
    path("dishes/", DishListView.as_view(), name="dishes_list"),

    path("orders/create/", OrderCreateView.as_view(), name='order_create'),
]
