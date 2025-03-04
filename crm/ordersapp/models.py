from typing import List, Generator

from django.db import models
from django.db.models import Field


class Dish(models.Model):
    """
    Модель Dish представляет блюдо,
    которое можно заказать в кафе

    Заказы тут: :model:`ordersapp.Order`
    """

    class Meta:
        verbose_name_plural = "dishes"

    name: Field = models.CharField(max_length=100, db_index=True)
    description: Field = models.TextField(null=False, blank=True, db_index=True)
    price: Field = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price} руб"


class Order(models.Model):
    """
    Модель Order представляет заказ,
    в кафе
    """
    STATUS_CHOICES: List[tuple[str, str]] = [
        ("В ожидании", "В ожидании"),
        ("Готово", "Готово"),
        ("Оплачено", "Оплачено"),
    ]
    TABLE_CHOICES: Generator[int] = [
        (i, f"Стол {i}") for i in range(1, 10)
    ]
    table_number: Field = models.IntegerField(choices=TABLE_CHOICES, db_index=True)
    items: Field = models.ManyToManyField(Dish, related_name='orders')
    total_price: Field = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    status: Field = models.CharField(max_length=10, choices=STATUS_CHOICES, default="В ожидании", db_index=True)

    def __str__(self):
        return f"Заказ {self.pk} - Стол {self.table_number} ({self.status})"
