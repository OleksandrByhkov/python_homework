from django.urls import path
from .views import (AdjustStockView, CancelReservationView, ConfirmReservationView,
                    ReservationListCreateView, StockDetailView, StockListCreateView)

urlpatterns = [
    path("stocks/", StockListCreateView.as_view(), name="stock-list"),
    path("stocks/<int:book_id>/", StockDetailView.as_view(), name="stock-detail"),
    path("stocks/<int:book_id>/adjust/", AdjustStockView.as_view(), name="stock-adjust"),
    path("reservations/", ReservationListCreateView.as_view(), name="reservation-list"),
    path("reservations/<uuid:pk>/confirm/", ConfirmReservationView.as_view(), name="reservation-confirm"),
    path("reservations/<uuid:pk>/cancel/", CancelReservationView.as_view(), name="reservation-cancel"),
]
