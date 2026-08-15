from celery import shared_task
from django.utils import timezone
from .models import Reservation
from .services import change_reservation_status

@shared_task
def expire_reservations():
    reservations = Reservation.objects.filter(status=Reservation.Status.PENDING, expires_at__lte=timezone.now())
    count = 0
    for reservation in reservations:
        change_reservation_status(reservation, Reservation.Status.EXPIRED)
        count += 1
    return count
