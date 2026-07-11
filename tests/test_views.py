import pytest
from django.urls import reverse

from tests.factories import BookFactory


pytestmark = pytest.mark.django_db


def test_book_list_view_returns_status_200(client):
    url = reverse("catalog:book_list")

    response = client.get(url)

    assert response.status_code == 200

def test_book_list_view_uses_correct_template(client):
    url = reverse("catalog:book_list")

    response = client.get(url)

    assert "catalog/book_list.html" in [
        template.name
        for template in response.templates
        if template.name
    ]

def test_book_list_view_contains_book(client):
    book = BookFactory(title="Python для всіх")
    url = reverse("catalog:book_list")

    response = client.get(url)

    assert response.status_code == 200
    assert "Python для всіх" in response.content.decode("utf-8")

def test_book_detail_view_returns_status_200(client):
    book = BookFactory()
    url = reverse("catalog:book_detail", kwargs={"pk": book.pk})

    response = client.get(url)

    assert response.status_code == 200

def test_book_detail_view_contains_book_title(client):
    book = BookFactory(title="Вивчаємо Django")
    url = reverse("catalog:book_detail", kwargs={"pk": book.pk})

    response = client.get(url)

    assert response.status_code == 200
    assert "Вивчаємо Django" in response.content.decode("utf-8")

def test_book_detail_view_returns_404_for_unknown_book(client):
    url = reverse("catalog:book_detail", kwargs={"pk": 999999})

    response = client.get(url)

    assert response.status_code == 404