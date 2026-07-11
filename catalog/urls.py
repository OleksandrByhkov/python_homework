from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    AsyncBookListView,
    AsyncBookDetailView,
    AsyncBookStatsView,
)
from .views import cart_add, cart_remove, cart_detail
from .views import order_create, payment_success, payment_cancel

app_name = "catalog"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/create/", BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:book_id>/", cart_add, name="cart_add"),
    path("cart/remove/<int:book_id>/", cart_remove, name="cart_remove"),
    path("order/create/", order_create, name="order_create"),
    path("payment/success/", payment_success, name="payment_success"),
    path("payment/cancel/", payment_cancel, name="payment_cancel"),
    path(
        "async/books/",
        AsyncBookListView.as_view(),
        name="async_book_list",
    ),
    path(
        "async/books/<int:pk>/",
        AsyncBookDetailView.as_view(),
        name="async_book_detail",
    ),
    path(
        "async/stats/",
        AsyncBookStatsView.as_view(),
        name="async_book_stats",
    ),
]

