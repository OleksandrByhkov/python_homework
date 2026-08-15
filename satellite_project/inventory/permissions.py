from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsWarehouseManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_superuser or request.user.groups.filter(name="Warehouse Managers").exists()

class CanOperateReservations(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.groups.filter(name__in=("Warehouse Managers", "Warehouse Operators")).exists()
