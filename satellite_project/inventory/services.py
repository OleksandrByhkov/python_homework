from django.core.cache import cache
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Reservation, Stock, StockMovement

def invalidate_stock(book_id):
    cache.delete(f"stock:{book_id}")

@transaction.atomic
def adjust_stock(stock, delta, reason, user=None):
    stock = Stock.objects.select_for_update().get(pk=stock.pk)
    if stock.quantity + delta < stock.reserved:
        raise ValidationError("Quantity cannot be lower than reserved stock.")
    stock.quantity += delta
    stock.save(update_fields=["quantity", "updated_at"])
    StockMovement.objects.create(stock=stock, delta=delta, reason=reason, created_by=user)
    invalidate_stock(stock.book_id)
    return stock

@transaction.atomic
def reserve_stock(*, stock, order_id, quantity, user=None):
    stock = Stock.objects.select_for_update().get(pk=stock.pk)
    if quantity > stock.available:
        raise ValidationError("Not enough stock available.")
    reservation = Reservation.objects.create(stock=stock, order_id=order_id, quantity=quantity, created_by=user)
    stock.reserved += quantity
    stock.save(update_fields=["reserved", "updated_at"])
    invalidate_stock(stock.book_id)
    return reservation

@transaction.atomic
def change_reservation_status(reservation, new_status):
    reservation = Reservation.objects.select_for_update().select_related("stock").get(pk=reservation.pk)
    if reservation.status != Reservation.Status.PENDING:
        raise ValidationError("Only pending reservations can be changed.")
    stock = Stock.objects.select_for_update().get(pk=reservation.stock_id)
    stock.reserved -= reservation.quantity
    if new_status == Reservation.Status.CONFIRMED:
        stock.quantity -= reservation.quantity
    stock.save(update_fields=["quantity", "reserved", "updated_at"])
    reservation.status = new_status
    reservation.save(update_fields=["status"])
    invalidate_stock(stock.book_id)
    return reservation
