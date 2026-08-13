import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Book, Category, Order
from tests.factories import BookFactory, CategoryFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="apiuser",
        email="apiuser@example.com",
        password="StrongPassword123",
    )


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="AdminPassword123",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


def test_jwt_token_obtain(api_client, user):
    response = api_client.post(
        reverse("api:token_obtain_pair"),
        {
            "username": "apiuser",
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


def test_jwt_token_rejects_wrong_password(api_client, user):
    response = api_client.post(
        reverse("api:token_obtain_pair"),
        {
            "username": "apiuser",
            "password": "WrongPassword",
        },
        format="json",
    )

    assert response.status_code == 401


def test_anonymous_user_cannot_list_books(api_client):
    response = api_client.get(reverse("api:book-list"))

    assert response.status_code == 401


def test_authenticated_user_can_list_books(authenticated_client):
    BookFactory.create_batch(3)

    response = authenticated_client.get(reverse("api:book-list"))

    assert response.status_code == 200
    assert response.data["count"] == 3


def test_authenticated_user_can_retrieve_book(authenticated_client):
    book = BookFactory()

    response = authenticated_client.get(
        reverse(
            "api:book-detail",
            kwargs={"pk": book.pk},
        )
    )

    assert response.status_code == 200
    assert response.data["id"] == book.id
    assert response.data["title"] == book.title


def test_regular_user_cannot_create_book(
    authenticated_client,
):
    category = CategoryFactory()

    response = authenticated_client.post(
        reverse("api:book-list"),
        {
            "title": "REST API Book",
            "author": "Test Author",
            "description": "Test description",
            "price": "250.00",
            "stock": 5,
            "category_id": category.pk,
        },
        format="json",
    )

    assert response.status_code == 403


def test_admin_can_create_book(admin_client):
    category = CategoryFactory()

    response = admin_client.post(
        reverse("api:book-list"),
        {
            "title": "REST API Book",
            "author": "Test Author",
            "description": "Test description",
            "price": "250.00",
            "stock": 5,
            "category_id": category.pk,
        },
        format="json",
    )

    assert response.status_code == 201
    assert Book.objects.filter(title="REST API Book").exists()


def test_admin_can_update_book(admin_client):
    book = BookFactory()
    category = CategoryFactory()

    response = admin_client.patch(
        reverse(
            "api:book-detail",
            kwargs={"pk": book.pk},
        ),
        {
            "title": "Updated title",
            "category_id": category.pk,
        },
        format="json",
    )

    assert response.status_code == 200

    book.refresh_from_db()
    assert book.title == "Updated title"


def test_admin_can_delete_book(admin_client):
    book = BookFactory()

    response = admin_client.delete(
        reverse(
            "api:book-detail",
            kwargs={"pk": book.pk},
        )
    )

    assert response.status_code == 204
    assert not Book.objects.filter(pk=book.pk).exists()


def test_book_response_contains_nested_category(
    authenticated_client,
):
    category = CategoryFactory(
        name="Programming",
        slug="programming",
    )
    book = BookFactory(category=category)

    response = authenticated_client.get(
        reverse(
            "api:book-detail",
            kwargs={"pk": book.pk},
        )
    )

    assert response.status_code == 200
    assert response.data["category"]["id"] == category.id
    assert response.data["category"]["name"] == "Programming"


def test_authenticated_user_can_list_categories(authenticated_client):
    CategoryFactory.create_batch(3)

    response = authenticated_client.get(reverse("api:category-list"))

    assert response.status_code == 200
    assert response.data["count"] == 3


def test_regular_user_cannot_create_category(authenticated_client):
    response = authenticated_client.post(
        reverse("api:category-list"),
        {
            "name": "New category",
            "slug": "new-category",
        },
        format="json",
    )

    assert response.status_code == 403


def test_admin_can_create_category(admin_client):
    response = admin_client.post(
        reverse("api:category-list"),
        {
            "name": "Programming",
            "slug": "programming-api",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Category.objects.filter(slug="programming-api").exists()


def test_admin_can_update_category(admin_client):
    category = CategoryFactory()

    response = admin_client.patch(
        reverse(
            "api:category-detail",
            kwargs={"pk": category.pk},
        ),
        {
            "name": "Updated category",
        },
        format="json",
    )

    assert response.status_code == 200

    category.refresh_from_db()
    assert category.name == "Updated category"


def test_admin_can_delete_category(admin_client):
    category = CategoryFactory()

    response = admin_client.delete(
        reverse(
            "api:category-detail",
            kwargs={"pk": category.pk},
        )
    )

    assert response.status_code == 204
    assert not Category.objects.filter(pk=category.pk).exists()


def test_book_filter_by_author(authenticated_client):
    BookFactory(title="Book One", author="Robert Martin")
    BookFactory(title="Book Two", author="Other Author")

    response = authenticated_client.get(
        reverse("api:book-list"),
        {"author": "Robert Martin"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "Book One"


def test_book_filter_by_category(authenticated_client):
    category_one = CategoryFactory()
    category_two = CategoryFactory()

    book_one = BookFactory(category=category_one)
    BookFactory(category=category_two)

    response = authenticated_client.get(
        reverse("api:book-list"),
        {"category": category_one.pk},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == book_one.id


def test_book_search_by_title(authenticated_client):
    required_book = BookFactory(title="Django REST Framework")
    BookFactory(title="Python Basics")

    response = authenticated_client.get(
        reverse("api:book-list"),
        {"search": "Django"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == required_book.id


def test_book_ordering_by_price(authenticated_client):
    BookFactory(title="Expensive", price="500.00")
    BookFactory(title="Cheap", price="100.00")

    response = authenticated_client.get(
        reverse("api:book-list"),
        {"ordering": "price"},
    )

    assert response.status_code == 200
    assert response.data["results"][0]["title"] == "Cheap"


def test_book_pagination_is_20_items(authenticated_client):
    BookFactory.create_batch(25)

    response = authenticated_client.get(reverse("api:book-list"))

    assert response.status_code == 200
    assert response.data["count"] == 25
    assert len(response.data["results"]) == 20


def test_authenticated_user_can_view_empty_cart(authenticated_client):
    response = authenticated_client.get(reverse("api:cart-list"))

    assert response.status_code == 200
    assert response.data["items"] == []


def test_user_can_add_book_to_cart(authenticated_client):
    book = BookFactory()

    response = authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": book.pk,
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == 200


def test_cart_contains_added_book(authenticated_client):
    book = BookFactory(title="Cart API Book")

    authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": book.pk,
            "quantity": 2,
        },
        format="json",
    )

    response = authenticated_client.get(reverse("api:cart-list"))

    assert response.status_code == 200
    assert len(response.data["items"]) == 1
    assert response.data["items"][0]["book"]["title"] == "Cart API Book"
    assert response.data["items"][0]["quantity"] == 2


def test_cart_add_requires_book_id(authenticated_client):
    response = authenticated_client.post(
        reverse("api:cart-add"),
        {
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == 400


def test_cart_add_rejects_invalid_quantity(authenticated_client):
    book = BookFactory()

    response = authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": book.pk,
            "quantity": 0,
        },
        format="json",
    )

    assert response.status_code == 400


def test_cart_add_returns_404_for_unknown_book(authenticated_client):
    response = authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": 999999,
            "quantity": 1,
        },
        format="json",
    )

    assert response.status_code == 404


def test_user_can_remove_book_from_cart(authenticated_client):
    book = BookFactory()

    authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": book.pk,
            "quantity": 1,
        },
        format="json",
    )

    response = authenticated_client.post(
        reverse("api:cart-remove"),
        {
            "book_id": book.pk,
        },
        format="json",
    )

    assert response.status_code == 200

    cart_response = authenticated_client.get(reverse("api:cart-list"))

    assert cart_response.data["items"] == []


def test_user_can_clear_cart(authenticated_client):
    first_book = BookFactory()
    second_book = BookFactory()

    authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": first_book.pk,
            "quantity": 1,
        },
        format="json",
    )

    authenticated_client.post(
        reverse("api:cart-add"),
        {
            "book_id": second_book.pk,
            "quantity": 1,
        },
        format="json",
    )

    response = authenticated_client.post(
        reverse("api:cart-clear"),
        format="json",
    )

    assert response.status_code == 200

    cart_response = authenticated_client.get(reverse("api:cart-list"))

    assert cart_response.data["items"] == []


def test_authenticated_user_can_create_order(authenticated_client, user):
    response = authenticated_client.post(
        reverse("api:order-list"),
        {
            "first_name": "Іван",
            "last_name": "Петренко",
            "email": "ivan@example.com",
            "address": "Київ, Хрещатик 1",
            "status": "created",
        },
        format="json",
    )

    assert response.status_code == 201

    order = Order.objects.get(pk=response.data["id"])
    assert order.user == user
    assert order.first_name == "Іван"


def test_user_can_list_only_own_orders(
    authenticated_client,
    user,
    django_user_model,
):
    other_user = django_user_model.objects.create_user(
        username="otheruser",
        password="StrongPassword123",
    )

    own_order = Order.objects.create(
        user=user,
        first_name="Іван",
        last_name="Петренко",
        email="ivan@example.com",
        address="Київ",
    )

    Order.objects.create(
        user=other_user,
        first_name="Олена",
        last_name="Коваль",
        email="olena@example.com",
        address="Львів",
    )

    response = authenticated_client.get(reverse("api:order-list"))

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == own_order.id


def test_user_can_retrieve_own_order(
    authenticated_client,
    user,
):
    order = Order.objects.create(
        user=user,
        first_name="Іван",
        last_name="Петренко",
        email="ivan@example.com",
        address="Київ",
    )

    response = authenticated_client.get(
        reverse(
            "api:order-detail",
            kwargs={"pk": order.pk},
        )
    )

    assert response.status_code == 200
    assert response.data["id"] == order.id


def test_user_cannot_retrieve_other_users_order(
    authenticated_client,
    django_user_model,
):
    other_user = django_user_model.objects.create_user(
        username="owner2",
        password="StrongPassword123",
    )

    order = Order.objects.create(
        user=other_user,
        first_name="Олена",
        last_name="Коваль",
        email="olena@example.com",
        address="Львів",
    )

    response = authenticated_client.get(
        reverse(
            "api:order-detail",
            kwargs={"pk": order.pk},
        )
    )

    assert response.status_code == 404


def test_user_can_update_own_order(
    authenticated_client,
    user,
):
    order = Order.objects.create(
        user=user,
        first_name="Іван",
        last_name="Петренко",
        email="ivan@example.com",
        address="Київ",
    )

    response = authenticated_client.patch(
        reverse(
            "api:order-detail",
            kwargs={"pk": order.pk},
        ),
        {
            "address": "Одеса",
        },
        format="json",
    )

    assert response.status_code == 200

    order.refresh_from_db()
    assert order.address == "Одеса"


def test_user_cannot_update_other_users_order(
    authenticated_client,
    django_user_model,
):
    other_user = django_user_model.objects.create_user(
        username="owner3",
        password="StrongPassword123",
    )

    order = Order.objects.create(
        user=other_user,
        first_name="Олена",
        last_name="Коваль",
        email="olena@example.com",
        address="Львів",
    )

    response = authenticated_client.patch(
        reverse(
            "api:order-detail",
            kwargs={"pk": order.pk},
        ),
        {
            "address": "Одеса",
        },
        format="json",
    )

    assert response.status_code == 404


def test_admin_can_list_all_orders(
    admin_client,
    user,
    django_user_model,
):
    other_user = django_user_model.objects.create_user(
        username="otheradmincheck",
        password="StrongPassword123",
    )

    Order.objects.create(
        user=user,
        first_name="Іван",
        last_name="Петренко",
        email="ivan@example.com",
        address="Київ",
    )

    Order.objects.create(
        user=other_user,
        first_name="Олена",
        last_name="Коваль",
        email="olena@example.com",
        address="Львів",
    )

    response = admin_client.get(reverse("api:order-list"))

    assert response.status_code == 200
    assert response.data["count"] == 2


def test_order_filter_by_status(
    authenticated_client,
    user,
):
    Order.objects.create(
        user=user,
        first_name="Іван",
        last_name="Петренко",
        email="ivan@example.com",
        address="Київ",
        status="created",
    )

    paid_order = Order.objects.create(
        user=user,
        first_name="Олена",
        last_name="Коваль",
        email="olena@example.com",
        address="Львів",
        status="paid",
    )

    response = authenticated_client.get(
        reverse("api:order-list"),
        {"status": "paid"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == paid_order.id
