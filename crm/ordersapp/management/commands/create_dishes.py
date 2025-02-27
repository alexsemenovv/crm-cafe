import random

from django.core.management import BaseCommand

from ordersapp.models import Dish


class Command(BaseCommand):
    """
    Создание блюд
    """

    def handle(self, *args, **options):
        self.stdout.write("Создаём блюда")
        dishes = [
            'Запеканка',
            'Плов',
            'Борщ',
            'Омлет',
            'Шаурма',
        ]
        for dish_name in dishes:
            rand_price = round(random.randint(200, 500) + random.random(), 2)
            dish, created = Dish.objects.get_or_create(name=dish_name, price=rand_price)
            self.stdout.write(f"Создано блюдо {dish.name}")
        self.stdout.write(self.style.SUCCESS("Блюда созданы"))
