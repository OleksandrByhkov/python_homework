from decimal import Decimal

import pytest
from django.db import IntegrityError

from catalog.models import Book, Category, Order, OrderItem
from tests.factories import (
    BookFactory,
    CategoryFactory,
    OrderFactory,
    OrderItemFactory,
)

pytestmark = pytest.mark.django_db


def test_category_is_created():
    # Generated with AI, reviewed and modified
    category = CategoryFactory()

    assert Category.objects.count() == 1
    assert category.pk is not None


def test_category_str_returns_name():
    # Generated with AI, reviewed and modified
    category = CategoryFactory(name="Програмування")

    assert str(category) == "Програмування"


def test_category_slug_is_saved():
    category = CategoryFactory(slug="programming")

    assert category.slug == "programming"


def test_category_slug_must_be_unique():
    CategoryFactory(slug="fiction")

    with pytest.raises(IntegrityError):
        CategoryFactory(slug="fiction")


def test_book_is_created():
    book = BookFactory()

    assert Book.objects.count() == 1
    assert book.pk is not None


def test_book_str_returns_title():
    book = BookFactory(title="Чистий код")

    assert str(book) == "Чистий код"


def test_book_has_correct_price():
    book = BookFactory(price=Decimal("399.99"))

    assert book.price == Decimal("399.99")


def test_book_belongs_to_category():
    category = CategoryFactory(name="Фантастика")
    book = BookFactory(category=category)

    assert book.category == category
    assert book in category.books.all()


def test_order_is_created():
    # Generated with AI, reviewed and modified
    order = OrderFactory()

    assert Order.objects.count() == 1
    assert order.pk is not None


def test_order_str_returns_id_and_email():
    # Generated with AI, reviewed and modified
    order = OrderFactory(email="customer@example.com")

    assert str(order) == f"Order #{order.id} - customer@example.com"


def test_order_default_status_is_created():
    # Generated with AI, reviewed and modified
    order = OrderFactory()

    assert order.status == "created"
    assert order.paid is False


def test_order_item_is_created():
    # Generated with AI, reviewed and modified
    item = OrderItemFactory()

    assert OrderItem.objects.count() == 1
    assert item.pk is not None


def test_order_item_get_cost():
    # Generated with AI, reviewed and modified
    item = OrderItemFactory(
        price=Decimal("125.50"),
        quantity=3,
    )

    assert item.get_cost() == Decimal("376.50")


def test_order_item_str():
    # Generated with AI, reviewed and modified
    book = BookFactory(title="Django для початківців")

    item = OrderItemFactory(
        book=book,
        quantity=2,
    )

    assert str(item) == "Django для початківців x 2"


def test_order_total_cost():
    # Generated with AI, reviewed and modified
    order = OrderFactory()

    OrderItemFactory(
        order=order,
        price=Decimal("100.00"),
        quantity=2,
    )

    OrderItemFactory(
        order=order,
        price=Decimal("150.00"),
        quantity=1,
    )

    assert order.get_total_cost() == Decimal("350.00")
