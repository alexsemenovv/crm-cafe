import random
from typing import Sequence

from django.core.management import BaseCommand

from ordersapp.models import Order, Dish


class Command(BaseCommand):
    """
    Создание заказов
    """

    def handle(self, *args, **options):
        self.stdout.write("Создаём заказы")
        all_dishes: Sequence[Dish] = list(Dish.objects.only('id').all())
        for _ in range(3):
            table = random.randint(1, 8)
            dishes = random.sample(all_dishes, 2)
            order, created = Order.objects.get_or_create(table_number=table)
            order.items.add(*dishes)
            self.stdout.write(f"Создан заказ {order.id}")
        self.stdout.write(self.style.SUCCESS("Заказы созданы"))
