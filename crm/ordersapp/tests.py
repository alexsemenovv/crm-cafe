from string import ascii_letters
from random import choices

from django.test import TestCase
from django.urls import reverse

from .models import Dish


class DishCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        """
        Настройка перед запуском теста
        """
        self.dish_name = "".join(choices(ascii_letters, k=10))  # создаём случайную строку
        Dish.objects.filter(name=self.dish_name).delete()

    def test_create_dish(self):
        """
        Тест на создание и добавление в БД нового блюда
        """
        response = self.client.post(
            reverse('ordersapp:dish_create'),
            {
                "name": self.dish_name,
                "description": "Новое супервкусное блюдо",
                "price": "587"
            }
        )
        self.assertRedirects(response, reverse("ordersapp:dishes_list"))
        self.assertTrue(
            Dish.objects.filter(name=self.dish_name).exists()
        )
