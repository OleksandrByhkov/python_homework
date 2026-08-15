from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid
import inventory.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Stock", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("book_id", models.PositiveBigIntegerField(unique=True)), ("title", models.CharField(blank=True, max_length=255)),
            ("quantity", models.PositiveIntegerField(default=0)), ("reserved", models.PositiveIntegerField(default=0)),
            ("updated_at", models.DateTimeField(auto_now=True)),
        ], options={"permissions": [("adjust_stock", "Can adjust warehouse stock")]}),
        migrations.CreateModel(name="Reservation", fields=[
            ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ("order_id", models.CharField(max_length=100, unique=True)), ("quantity", models.PositiveIntegerField()),
            ("status", models.CharField(choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled"), ("expired", "Expired")], default="pending", max_length=12)),
            ("expires_at", models.DateTimeField(default=inventory.models.reservation_expiry)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ("stock", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reservations", to="inventory.stock")),
        ]),
        migrations.CreateModel(name="StockMovement", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("delta", models.IntegerField()), ("reason", models.CharField(max_length=255)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("created_by", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ("stock", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="movements", to="inventory.stock")),
        ]),
    ]
