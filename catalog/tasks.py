import csv
from pathlib import Path

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command
from django.utils import timezone

from .models import Order


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_order_confirmation_email(order_id):
    """
    Send an order confirmation email asynchronously.
    """

    order = Order.objects.get(pk=order_id)

    send_mail(
        subject=f"Замовлення #{order.id} створено",
        message=(
            f"Ваше замовлення #{order.id} успішно створено.\n"
            f"Загальна сума: {order.get_total_cost()} грн."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.email],
        fail_silently=False,
    )

    return f"Email sent for order {order.id}"


@shared_task
def generate_orders_report():
    """
    Generate a CSV report containing all orders.
    """

    reports_directory = (
        Path(settings.BASE_DIR)
        / "reports"
    )
    reports_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        reports_directory
        / f"orders_{timezone.now():%Y-%m-%d_%H-%M-%S}.csv"
    )

    orders = Order.objects.select_related("user").all()

    with filename.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as report_file:
        writer = csv.writer(report_file)

        writer.writerow([
            "ID",
            "User",
            "Email",
            "Status",
            "Paid",
            "Created at",
            "Total cost",
        ])

        for order in orders:
            writer.writerow([
                order.id,
                order.user.username if order.user else "",
                order.email,
                order.status,
                order.paid,
                order.created_at,
                order.get_total_cost(),
            ])

    return str(filename)


@shared_task
def clear_expired_sessions():
    """
    Remove expired Django sessions.
    """

    call_command("clearsessions")

    return "Expired sessions cleared"