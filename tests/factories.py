from decimal import Decimal

import factory

from catalog.models import Book, Category
from catalog.models import Book, Category, Order, OrderItem


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda number: f"Категорія {number}")
    slug = factory.Sequence(lambda number: f"category-{number}")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda number: f"Книга {number}")
    author = factory.Sequence(lambda number: f"Автор {number}")
    description = "Тестовий опис книги"
    price = Decimal("250.00")
    stock = 10
    category = factory.SubFactory(CategoryFactory)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    first_name = "Іван"
    last_name = "Петренко"
    email = factory.Sequence(
        lambda number: f"customer{number}@example.com"
    )
    address = "Київ, Хрещатик 1"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    book = factory.SubFactory(BookFactory)
    price = Decimal("250.00")
    quantity = 1