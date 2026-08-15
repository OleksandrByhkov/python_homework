import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from inventory.models import Reservation, Stock

@pytest.fixture
def manager(db):
    user = User.objects.create_user("manager", "manager@example.com", "safe-password")
    group, _ = Group.objects.get_or_create(name="Warehouse Managers")
    user.groups.add(group)
    return user

@pytest.fixture
def client(manager):
    api = APIClient()
    api.force_authenticate(manager)
    return api

@pytest.mark.django_db
def test_jwt_login():
    User.objects.create_user("alex", "alex@example.com", "safe-password")
    response = APIClient().post(reverse("token"), {"username": "alex", "password": "safe-password"})
    assert response.status_code == 200 and "access" in response.data

@pytest.mark.django_db
def test_stock_crud_and_available(client):
    assert client.post(reverse("stock-list"), {"book_id": 42, "title": "Django", "quantity": 10}).status_code == 201
    assert client.get(reverse("stock-detail", args=[42])).data["available"] == 10

@pytest.mark.django_db
def test_adjust_stock_creates_movement(client):
    stock = Stock.objects.create(book_id=1, quantity=5)
    response = client.post(reverse("stock-adjust", args=[1]), {"delta": 3, "reason": "delivery"})
    stock.refresh_from_db()
    assert response.status_code == 200 and stock.quantity == 8 and stock.movements.count() == 1

@pytest.mark.django_db
def test_reservation_confirm_flow(client):
    stock = Stock.objects.create(book_id=7, quantity=5)
    response = client.post(reverse("reservation-list"), {"book_id": 7, "order_id": "ORDER-1", "quantity": 2})
    reservation = Reservation.objects.get(order_id="ORDER-1")
    assert response.status_code == 201
    assert client.post(reverse("reservation-confirm", args=[reservation.pk])).status_code == 200
    stock.refresh_from_db(); reservation.refresh_from_db()
    assert reservation.status == Reservation.Status.CONFIRMED and (stock.quantity, stock.reserved) == (3, 0)

@pytest.mark.django_db
def test_rejects_overbooking(client):
    Stock.objects.create(book_id=9, quantity=1)
    assert client.post(reverse("reservation-list"), {"book_id": 9, "order_id": "ORDER-2", "quantity": 2}).status_code == 400

@pytest.mark.django_db
def test_permissions(manager):
    assert APIClient().get(reverse("stock-list")).status_code == 401
    user = User.objects.create_user("viewer", "viewer@example.com", "safe-password")
    api = APIClient(); api.force_authenticate(user)
    assert api.post(reverse("stock-list"), {"book_id": 1, "quantity": 1}).status_code == 403
