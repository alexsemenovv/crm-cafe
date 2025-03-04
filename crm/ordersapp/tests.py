from random import choices, randint
from string import ascii_letters

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from .models import Dish, Order


class DishCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        """
        Настройка перед запуском теста.
        Генерируем случайное имя для блюда
        """
        self.dish_name = "".join(
            choices(ascii_letters, k=10)
        )  # создаём случайную строку

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
            reverse("ordersapp:dish_create"),
            {
                "name": self.dish_name,
                "description": "Новое супервкусное блюдо",
                "price": "587",
            },
        )
        self.assertRedirects(response, reverse("ordersapp:dishes_list"))
        self.assertTrue(Dish.objects.filter(name=self.dish_name).exists())


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
        response = self.client.get(
            reverse("ordersapp:dishes_list")
        )  # делаем запрос на страницу
        self.assertQuerySetEqual(
            qs=list(Dish.objects.filter(name__contains="Блюдо").all()),
            values=(d.pk for d in response.context["dishes"]),
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
            Dish.objects.create(
                name=f"Блюдо #{i}",
                price=i,
            )
            for i in range(3)
        ]

    @classmethod
    def tearDown(cls):
        """
        Удаляем блюда после теста
        """
        for dish in cls.dishes:
            dish.delete()

    def test_create_order(self):
        """
        Тест на создание и добавление в БД нового заказа
        """
        response = self.client.post(
            reverse("ordersapp:order_create"),
            {
                "table_number": randint(1, 9),
                "items": self.dishes,
            },
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
        cls.dish = [
            Dish.objects.create(
                name=f"Блюдо для теста",
                price=0,
            )
        ]

        # создаём 3 заказа с одинаковым блюдом
        cls.orders = [Order.objects.create(table_number=i) for i in range(1, 4)]
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
        response = self.client.get(
            reverse("ordersapp:orders_list")
        )  # делаем запрос на страницу
        self.assertQuerySetEqual(
            qs=list(Order.objects.filter(total_price="0").all()),
            values=(d.pk for d in response.context["orders"]),
            transform=lambda d: d.pk,
        )
        self.assertTemplateUsed(response, "ordersapp/orders_list.html")


class OrderDeleteViewTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        """
        Настройка перед запуском теста
        """

        # создаём блюдо для заказа
        cls.dish = [
            Dish.objects.create(
                name="Блюдо для теста",
                price=0,
            )
        ]

        # создаём заказ
        cls.order = Order.objects.create(table_number=1)
        cls.order.items.set(cls.dish)

    @classmethod
    def tearDown(cls):
        """
        Удаляем блюдо после теста
        """
        cls.dish[0].delete()

    def test_delete_order(self):
        """Тестирование удаления заказа"""
        response = self.client.post(
            reverse("ordersapp:order_delete", kwargs={"pk": self.order.pk})
        )  # Отправляем POST-запрос на удаление
        self.assertRedirects(
            response, reverse("ordersapp:orders_list")
        )  # Проверяем редирект
        self.assertFalse(
            Order.objects.filter(pk=self.order.pk).exists()
        )  # Проверяем, что заказ удален

    def test_delete_nonexistent_order(self):
        """Попытка удалить несуществующий заказ должна вернуть 404"""
        non_existing_url = reverse("ordersapp:order_delete", kwargs={"pk": 9999999})
        response = self.client.post(non_existing_url)
        self.assertEqual(response.status_code, 404)


class OrderUpdateViewTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        """
        Настройка перед запуском теста
        """

        # создаём блюдо для заказа
        cls.dish = [
            Dish.objects.create(
                name="Блюдо для теста",
                price=0,
            )
        ]

        # создаём заказ
        cls.order = Order.objects.create(table_number=1)
        cls.order.items.set(cls.dish)

    @classmethod
    def tearDown(cls):
        """
        Удаляем блюдо после теста
        """
        cls.dish[0].delete()

    def test_update_order(self):
        """Тестирование обновление статуса заказа"""
        response = self.client.post(
            reverse("ordersapp:order_update", kwargs={"pk": self.order.pk}),
            {"status": "Готово", "items": self.dish[0].pk},
        )  # Отправляем POST-запрос на обновление

        self.assertRedirects(
            response, reverse("ordersapp:orders_list")
        )  # Проверяем редирект
        self.assertTrue(
            Order.objects.filter(Q(pk=self.order.pk) & Q(status="Готово")).exists()
        )  # Проверяем, что статус обновлен


class OrderSearchListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создаем тестовые заказы"""
        cls.order1 = Order.objects.create(table_number=1, status="Готово")
        cls.order2 = Order.objects.create(table_number=2, status="Оплачено")

    def test_search_by_table_number(self):
        """Тест поиска заказа по номеру стола"""
        response = self.client.get(reverse("ordersapp:order_search"), {"q": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Готово"
        )  # Проверяем, что найден заказ со столом 1

    def test_search_by_status(self):
        """Тест поиска заказа по статусу"""
        response = self.client.get(reverse("ordersapp:order_search"), {"q": "Оплачено"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Оплачено"
        )  # Проверяем, что найден заказ со статусом "Оплачено"

    def test_search_no_results(self):
        """Тест поиска с несуществующим значением"""
        response = self.client.get(
            reverse("ordersapp:order_search"), {"q": "Неизвестный статус"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Готово")  # Не должно быть найденных заказов
        self.assertNotContains(response, "Оплачено")


class OrderTotalIncomesListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создаем тестовые оплаченные и неоплаченные заказы"""
        cls.order1 = Order.objects.create(
            table_number=1, status="Оплачено", total_price=100.50
        )
        cls.order2 = Order.objects.create(
            table_number=2, status="Оплачено", total_price=200.75
        )
        cls.order3 = Order.objects.create(
            table_number=3, status="Готово", total_price=50.00
        )  # Не должен считаться

    def test_total_income_calculation(self):
        """Тест подсчета общей выручки"""
        response = self.client.get(reverse("ordersapp:total_incomes"))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице есть сумма 301.25 (100.50 + 200.75)
        self.assertContains(response, "301.25")

    def test_only_paid_orders_are_counted(self):
        """Тест фильтрации: в список должны попадать только оплаченные заказы"""
        response = self.client.get(reverse("ordersapp:total_incomes"))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что есть только "Оплачено", но нет "Готово"
        self.assertContains(response, "Оплачено")
        self.assertNotContains(response, "Готово")

    def test_no_orders(self):
        """Тест страницы без заказов (если нет оплаченных заказов)"""
        Order.objects.all().delete()  # Удаляем все заказы
        response = self.client.get(reverse("ordersapp:total_incomes"))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице нет числа
        self.assertNotContains(response, "301.25")
