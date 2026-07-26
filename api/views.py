from django.shortcuts import render

# Create your views here.

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response

from catalog.cart import Cart
from catalog.models import Book, Category, Order

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    BookSerializer,
    CartSerializer,
    CategorySerializer,
    OrderSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for book categories.

    Reading requires authentication.
    Creating, updating and deleting categories requires admin access.
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    filterset_fields = ["name", "slug"]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "id"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint for books.

    Authenticated users can read books.
    Only admin users can create, update or delete books.
    """

    queryset = Book.objects.select_related("category").all().order_by("title")
    serializer_class = BookSerializer

    filterset_fields = [
        "category",
        "stock",
        "author",
    ]

    search_fields = [
        "title",
        "author",
        "description",
    ]

    ordering_fields = [
        "title",
        "author",
        "price",
        "stock",
    ]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for orders.

    Regular users can access only their own orders.
    Admin users can access all orders.
    """

    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    filterset_fields = [
        "status",
        "paid",
    ]

    ordering_fields = [
        "created_at",
        "status",
    ]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()
        queryset = Order.objects.prefetch_related(
            "items__book__category"
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ViewSet):
    """
    API endpoint for the session-based shopping cart.
    """

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = Cart(request)

        data = {
            "items": list(cart),
            "total_price": cart.get_total_price(),
        }

        serializer = CartSerializer(data)

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="add",
    )
    def add(self, request):
        book_id = request.data.get("book_id")
        quantity = request.data.get("quantity", 1)

        if not book_id:
            return Response(
                {"detail": "book_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"detail": "quantity must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {"detail": "quantity must be greater than 0."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.add(
            book=book,
            quantity=quantity,
        )

        return Response(
            {"detail": "Book added to cart."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="remove",
    )
    def remove(self, request):
        book_id = request.data.get("book_id")

        if not book_id:
            return Response(
                {"detail": "book_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.remove(book)

        return Response(
            {"detail": "Book removed from cart."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="clear",
    )
    def clear(self, request):
        cart = Cart(request)
        cart.clear()

        return Response(
            {"detail": "Cart cleared."},
            status=status.HTTP_200_OK,
        )