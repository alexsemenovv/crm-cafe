from django.urls import path

from .views import order_index

app_name = "ordersapp"

urlpatterns = [
    path("", order_index, name="index"),
]
