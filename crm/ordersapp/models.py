from django.db import models


class Dish(models.Model):
    """
    Модель Dish представляет блюдо,
    которое можно заказать в кафе

    Заказы тут: :model:`ordersapp.Order`
    """
    class Meta:
        verbose_name_plural = "dishes"

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель Order представляет заказ,
    в кафе
    """
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]
    table_number = models.IntegerField()
    items = models.ManyToManyField(Dish, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def total_price(self):
        """
        Вычисляет общую стоимость заказа
        :return: int
        """
        return (dish.price for dish in self.items.objects.all())

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number} ({self.get_status_display()})"
