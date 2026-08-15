from rest_framework import serializers
from .models import Reservation, Stock, StockMovement
from .services import reserve_stock

class StockSerializer(serializers.ModelSerializer):
    available = serializers.IntegerField(read_only=True)
    class Meta:
        model = Stock
        fields = ("id", "book_id", "title", "quantity", "reserved", "available", "updated_at")
        read_only_fields = ("reserved", "updated_at")

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ("id", "stock", "delta", "reason", "created_at")
        read_only_fields = ("created_at",)

class ReservationSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Reservation
        fields = ("id", "order_id", "book_id", "stock", "quantity", "status", "expires_at", "created_at")
        read_only_fields = ("id", "stock", "status", "expires_at", "created_at")

    def create(self, validated_data):
        book_id = validated_data.pop("book_id")
        try:
            stock = Stock.objects.get(book_id=book_id)
        except Stock.DoesNotExist as exc:
            raise serializers.ValidationError({"book_id": "Unknown book."}) from exc
        return reserve_stock(stock=stock, user=self.context["request"].user, **validated_data)
