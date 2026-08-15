from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_warehouse_groups(sender, **kwargs):
    if sender.name == "inventory":
        managers, _ = Group.objects.get_or_create(name="Warehouse Managers")
        operators, _ = Group.objects.get_or_create(name="Warehouse Operators")
        managers.permissions.set(Permission.objects.filter(content_type__app_label="inventory"))
        operators.permissions.set(Permission.objects.filter(
            content_type__app_label="inventory",
            codename__in=("view_stock", "view_reservation", "add_reservation", "change_reservation"),
        ))
