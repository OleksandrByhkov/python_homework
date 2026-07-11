from types import SimpleNamespace

import pytest
from django.urls import reverse

from catalog.models import Order, OrderItem
from tests.factories import BookFactory, CategoryFactory
from decimal import Decimal


pytestmark = pytest.mark.django_db


def test_user_can_open_book_list(client):
    response = client.get(reverse("catalog:book_list"))

    assert response.status_code == 200
    assert "catalog/book_list.html" in [
        template.name
        for template in response.templates
        if template.name
    ]

def test_user_can_search_book_by_title(client):
    required_book = BookFactory(title="Python для початківців")
    other_book = BookFactory(title="Історія України")

    response = client.get(
        reverse("catalog:book_list"),
        {"search": "Python"},
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert required_book.title in content
    assert other_book.title not in content

def test_user_can_search_book_by_author(client):
    required_book = BookFactory(
        title="Чистий код",
        author="Robert Martin",
    )
    other_book = BookFactory(
        title="Django",
        author="William Vincent",
    )

    response = client.get(
        reverse("catalog:book_list"),
        {"search": "Robert"},
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert required_book.title in content
    assert other_book.title not in content

def test_user_can_filter_books_by_category(client):
    programming = CategoryFactory(name="Програмування")
    fiction = CategoryFactory(name="Фантастика")

    programming_book = BookFactory(
        title="Вивчаємо Django",
        category=programming,
    )
    fiction_book = BookFactory(
        title="Дюна",
        category=fiction,
    )

    response = client.get(
        reverse("catalog:book_list"),
        {"category": programming.pk},
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert programming_book.title in content
    assert fiction_book.title not in content

def test_user_can_filter_available_books(client):
    available_book = BookFactory(
        title="Книга в наявності",
        stock=5,
    )
    unavailable_book = BookFactory(
        title="Книга відсутня",
        stock=0,
    )

    response = client.get(
        reverse("catalog:book_list"),
        {"available": "on"},
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert available_book.title in content
    assert unavailable_book.title not in content

def test_user_can_open_book_detail(client):
    book = BookFactory(
        title="Архітектура Django",
        author="Test Author",
    )

    response = client.get(
        reverse(
            "catalog:book_detail",
            kwargs={"pk": book.pk},
        )
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert book.title in content
    assert book.author in content

def test_user_can_log_in(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="StrongPassword123",
    )

    response = client.post(
        reverse("accounts:login"),
        {
            "username": "testuser",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 302
    assert str(user.pk) == client.session.get("_auth_user_id")

def test_user_can_log_out(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="logoutuser",
        email="logout@example.com",
        password="StrongPassword123",
    )

    client.force_login(user)

    response = client.post(reverse("accounts:logout"))

    assert response.status_code == 302
    assert "_auth_user_id" not in client.session

def test_anonymous_user_is_redirected_from_book_create(client):
    response = client.get(reverse("catalog:book_create"))

    assert response.status_code == 302
    assert reverse("accounts:login") in response.url

def test_user_can_add_book_to_cart(client):
    book = BookFactory(
        title="Книга у кошику",
        price="250.00",
        stock=10,
    )

    response = client.post(
        reverse(
            "catalog:cart_add",
            kwargs={"book_id": book.pk},
        ),
        {"quantity": 2},
        follow=True,
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert book.title in content

def test_user_can_remove_book_from_cart(client):
    book = BookFactory(
        title="Книга для видалення",
        price="150.00",
        stock=5,
    )

    client.post(
        reverse(
            "catalog:cart_add",
            kwargs={"book_id": book.pk},
        ),
        {"quantity": 1},
    )

    response = client.post(
        reverse(
            "catalog:cart_remove",
            kwargs={"book_id": book.pk},
        ),
        follow=True,
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert book.title not in content

def test_empty_cart_redirects_from_order_create(client):
    response = client.get(reverse("catalog:order_create"))

    assert response.status_code == 302
    assert response.url == reverse("catalog:book_list")

def test_user_can_open_order_form_with_cart_item(client):
    book = BookFactory(
        title="Книга для замовлення",
        price="300.00",
        stock=3,
    )

    client.post(
        reverse(
            "catalog:cart_add",
            kwargs={"book_id": book.pk},
        ),
        {"quantity": 1},
    )

    response = client.get(reverse("catalog:order_create"))

    assert response.status_code == 200
    assert "catalog/order_create.html" in [
        template.name
        for template in response.templates
        if template.name
    ]
    assert book.title in response.content.decode("utf-8")

def test_user_can_create_order_with_mocked_stripe_and_email(
    client,
    mocker,
):
    book = BookFactory(
        title="Тестова книга",
        price=Decimal("400.00"),
        stock=10,
    )

    client.post(
        reverse(
            "catalog:cart_add",
            kwargs={"book_id": book.pk},
        ),
        {"quantity": 2},
    )

    mocked_email = mocker.patch(
        "catalog.views.send_mail",
        return_value=1,
    )

    mocked_stripe = mocker.patch(
        "catalog.views.stripe.checkout.Session.create",
        return_value=SimpleNamespace(
            id="cs_test_123",
            url="https://stripe.example.com/test-checkout",
        ),
    )

    response = client.post(
        reverse("catalog:order_create"),
        {
            "first_name": "Іван",
            "last_name": "Петренко",
            "email": "ivan@example.com",
            "address": "Київ, Хрещатик 1",
        },
    )

    assert response.status_code == 302
    assert response.url == "https://stripe.example.com/test-checkout"

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1

    order = Order.objects.first()
    order_item = OrderItem.objects.first()

    assert order.first_name == "Іван"
    assert order.last_name == "Петренко"
    assert order.email == "ivan@example.com"
    assert order.address == "Київ, Хрещатик 1"
    assert order.stripe_session_id == "cs_test_123"

    assert order_item.order == order
    assert order_item.book == book
    assert order_item.quantity == 2
    assert order_item.price == book.price

    mocked_email.assert_called_once()
    mocked_stripe.assert_called_once()

def test_cart_is_cleared_after_order_creation(
    client,
    mocker,
):
    book = BookFactory(
        title="Книга перед очищенням кошика",
        price="200.00",
        stock=10,
    )

    client.post(
        reverse(
            "catalog:cart_add",
            kwargs={"book_id": book.pk},
        ),
        {"quantity": 1},
    )

    mocker.patch(
        "catalog.views.send_mail",
        return_value=1,
    )

    mocker.patch(
        "catalog.views.stripe.checkout.Session.create",
        return_value=SimpleNamespace(
            id="cs_test_clear_cart",
            url="https://stripe.example.com/clear-cart",
        ),
    )

    response = client.post(
        reverse("catalog:order_create"),
        {
            "first_name": "Олена",
            "last_name": "Коваль",
            "email": "olena@example.com",
            "address": "Львів, Центральна 10",
        },
    )

    assert response.status_code == 302

    cart_response = client.get(reverse("catalog:cart_detail"))
    content = cart_response.content.decode("utf-8")

    assert book.title not in content


def test_user_can_open_payment_result_pages(client):
    success_response = client.get(
        reverse("catalog:payment_success")
    )
    cancel_response = client.get(
        reverse("catalog:payment_cancel")
    )

    assert success_response.status_code == 200
    assert cancel_response.status_code == 200

    assert "catalog/payment_success.html" in [
        template.name
        for template in success_response.templates
        if template.name
    ]

    assert "catalog/payment_cancel.html" in [
        template.name
        for template in cancel_response.templates
        if template.name
    ]