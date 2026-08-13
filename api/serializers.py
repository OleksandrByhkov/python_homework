from rest_framework import serializers

from catalog.models import Book, Category, Order, OrderItem
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "description",
            "price",
            "stock",
            "category",
            "category_id",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "price",
            "quantity",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "email",
            "address",
            "created_at",
            "paid",
            "status",
            "stripe_session_id",
            "items",
            "total_cost",
        ]

        read_only_fields = [
            "user",
            "created_at",
            "paid",
            "stripe_session_id",
        ]

    @extend_schema_field(
        serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
        )
    )
    def get_total_cost(self, obj):
        return obj.get_total_cost()


class CartItemSerializer(serializers.Serializer):
    book = BookSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
