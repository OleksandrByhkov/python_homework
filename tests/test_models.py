from decimal import Decimal

import pytest
from django.db import IntegrityError

from catalog.models import Book, Category
from tests.factories import BookFactory, CategoryFactory


pytestmark = pytest.mark.django_db


def test_category_is_created():
    category = CategoryFactory()

    assert Category.objects.count() == 1
    assert category.pk is not None


def test_category_str_returns_name():
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