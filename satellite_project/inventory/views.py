from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reservation, Stock
from .permissions import CanOperateReservations, IsWarehouseManagerOrReadOnly
from .serializers import ReservationSerializer, StockSerializer
from .services import adjust_stock, change_reservation_status

class BaseStockView:
    queryset = Stock.objects.all().order_by("book_id")
    serializer_class = StockSerializer
    permission_classes = (IsWarehouseManagerOrReadOnly,)

class StockListCreateView(BaseStockView, generics.ListCreateAPIView):
    pass

class StockDetailView(BaseStockView, generics.RetrieveUpdateAPIView):
    lookup_field = "book_id"

    def retrieve(self, request, *args, **kwargs):
        key = f"stock:{kwargs['book_id']}"
        data = cache.get(key)
        if data is None:
            data = self.get_serializer(self.get_object()).data
            cache.set(key, data, 60)
        return Response(data)

class AdjustStockView(APIView):
    permission_classes = (IsWarehouseManagerOrReadOnly,)
    def post(self, request, book_id):
        stock = get_object_or_404(Stock, book_id=book_id)
        try:
            delta = int(request.data.get("delta"))
        except (TypeError, ValueError):
            return Response({"delta": "A valid integer is required."}, status=400)
        stock = adjust_stock(stock, delta, request.data.get("reason", "manual adjustment"), request.user)
        return Response(StockSerializer(stock).data)

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.select_related("stock").all().order_by("-created_at")
    serializer_class = ReservationSerializer
    permission_classes = (CanOperateReservations,)

class ReservationActionView(APIView):
    permission_classes = (CanOperateReservations,)
    action_status = None
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation = change_reservation_status(reservation, self.action_status)
        return Response(ReservationSerializer(reservation).data, status=status.HTTP_200_OK)

class ConfirmReservationView(ReservationActionView):
    action_status = Reservation.Status.CONFIRMED

class CancelReservationView(ReservationActionView):
    action_status = Reservation.Status.CANCELLED
