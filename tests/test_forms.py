from decimal import Decimal

import pytest

from catalog.forms import BookForm
from tests.factories import CategoryFactory


pytestmark = pytest.mark.django_db


def get_valid_book_data(category):
    return {
        "title": "Django для початківців",
        "author": "Тестовий автор",
        "description": "Корисна книга про Django",
        "price": "350.00",
        "stock": 5,
        "category": category.pk,
    }


def test_book_form_is_valid_with_correct_data():
    category = CategoryFactory()
    form = BookForm(data=get_valid_book_data(category))

    assert form.is_valid()


def test_book_form_saves_book():
    category = CategoryFactory()
    form = BookForm(data=get_valid_book_data(category))

    assert form.is_valid()

    book = form.save()

    assert book.pk is not None
    assert book.title == "Django для початківців"
    assert book.price == Decimal("350.00")


def test_book_form_is_invalid_without_title():
    category = CategoryFactory()
    data = get_valid_book_data(category)
    data["title"] = ""

    form = BookForm(data=data)

    assert not form.is_valid()
    assert "title" in form.errors


def test_book_form_is_invalid_without_author():
    category = CategoryFactory()
    data = get_valid_book_data(category)
    data["author"] = ""

    form = BookForm(data=data)

    assert not form.is_valid()
    assert "author" in form.errors


def test_book_form_is_invalid_without_price():
    category = CategoryFactory()
    data = get_valid_book_data(category)
    data["price"] = ""

    form = BookForm(data=data)

    assert not form.is_valid()
    assert "price" in form.errors


def test_book_form_is_invalid_without_category():
    category = CategoryFactory()
    data = get_valid_book_data(category)
    data["category"] = ""

    form = BookForm(data=data)

    assert not form.is_valid()
    assert "category" in form.errors