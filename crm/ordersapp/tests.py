from string import ascii_letters
from random import choices, randint

from django.test import TestCase
from django.urls import reverse

from .models import Dish, Order


class DishCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        """
        Настройка перед запуском теста.
        Генерируем случайное имя для блюда
        """
        self.dish_name = "".join(choices(ascii_letters, k=10))  # создаём случайную строку

    def tearDown(self) -> None:
        """
        Настройка после тестов.
        Удаляем блюдо с таким названием, если встретим
        """
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


class DishListViewTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        """
        Настройка перед запуском теста.
        Создаём 3 блюда
        """
        for i in range(3):
            Dish.objects.create(
                name=f"Блюдо №{i}",
                price=i,
            )

    @classmethod
    def tearDown(cls) -> None:
        """
        Удаляем все блюда после тестов,
        в именах которых встречается слово 'Блюдо'
        """
        Dish.objects.filter(name__contains="Блюдо").delete()

    def test_list_dishes(self) -> None:
        """
        Метод проверяет список блюд,
        а также используемый шаблон
        """
        response = self.client.get(reverse("ordersapp:dishes_list"))  # делаем запрос на страницу
        self.assertQuerySetEqual(
            qs=list(Dish.objects.filter(name__contains="Блюдо").all()),
            values=(d.pk for d in response.context['dishes']),
            transform=lambda d: d.pk,
        )
        self.assertTemplateUsed(response, "ordersapp/dishes_list.html")


class OrderCreateViewTestCase(TestCase):
    @classmethod
    def setUp(cls):
        """
        Создаём 3 новых блюда для добавления в заказ
        """
        cls.dishes = [
            Dish.objects.create(name=f"Блюдо #{i}", price=i, )
            for i in range(3)
        ]

    @classmethod
    def tearDown(cls):
        """
        Удаляем заказ после теста
        """
        for dish in cls.dishes:
            dish.delete()

    def test_create_order(self):
        """
        Тест на создание и добавление в БД нового заказа
        """
        response = self.client.post(
            reverse('ordersapp:order_create'),
            {
                "table_number": randint(1, 9),
                "items": self.dishes,
            }
        )
        self.assertEqual(response.status_code, 200)


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        """
        Настройка перед запуском теста.
        Создаём 3 заказа
        """

        # создаём блюдо для заказов
        cls.dish = [Dish.objects.create(
            name=f"Блюдо для теста",
            price=0,
        )]

        # создаём 3 заказа с одинаковым блюдом
        cls.orders = [
            Order.objects.create(table_number=i)
            for i in range(1, 4)
        ]
        for order in cls.orders:
            order.items.set(cls.dish)



    @classmethod
    def tearDown(cls) -> None:
        """
        Удаляем 'Блюда для теста',
        и заказы с 1-го по 3-ий
        """
        cls.dish[0].delete()
        for order in cls.orders:
            order.delete()

    def test_list_orders(self) -> None:
        """
        Метод проверяет список заказов, которые равны 0,
        а также используемый шаблон
        """
        response = self.client.get(reverse("ordersapp:orders_list"))  # делаем запрос на страницу
        self.assertQuerySetEqual(
            qs=list(Order.objects.filter(total_price="0").all()),
            values=(d.pk for d in response.context['orders']),
            transform=lambda d: d.pk,
        )
        self.assertTemplateUsed(response, "ordersapp/orders_list.html")
