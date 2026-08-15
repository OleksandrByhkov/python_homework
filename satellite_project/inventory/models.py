import uuid
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def reservation_expiry():
    return timezone.now() + timezone.timedelta(minutes=15)

class Stock(models.Model):
    book_id = models.PositiveBigIntegerField(unique=True, verbose_name=_("Book ID"))
    title = models.CharField(max_length=255, blank=True, verbose_name=_("Title"))
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    reserved = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available(self):
        return self.quantity - self.reserved

    class Meta:
        permissions = [("adjust_stock", "Can adjust warehouse stock")]

class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        CONFIRMED = "confirmed", _("Confirmed")
        CANCELLED = "cancelled", _("Cancelled")
        EXPIRED = "expired", _("Expired")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=100, unique=True)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, related_name="reservations")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    expires_at = models.DateTimeField(default=reservation_expiry)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

class StockMovement(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="movements")
    delta = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
