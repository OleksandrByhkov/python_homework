from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, Category
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST
from .cart import Cart

import stripe

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from .forms import OrderCreateForm
from .models import OrderItem


class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.select_related("category").all()

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        available = self.request.GET.get("available")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if available == "on":
            queryset = queryset.filter(stock__gt=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["search"] = self.request.GET.get("search", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["available"] = self.request.GET.get("available", "")

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    template_name = "catalog/book_form.html"
    fields = ["category", "title", "author", "price", "description", "stock"]
    success_url = reverse_lazy("catalog:book_list")
    permission_required = "catalog.can_manage_books"


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    template_name = "catalog/book_form.html"
    fields = ["category", "title", "author", "price", "description", "stock"]
    success_url = reverse_lazy("catalog:book_list")
    permission_required = "catalog.can_manage_books"


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = "catalog/book_confirm_delete.html"
    success_url = reverse_lazy("catalog:book_list")
    permission_required = "catalog.can_manage_books"

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    quantity = int(request.POST.get("quantity", 1))

    cart.add(book=book, quantity=quantity)

    return redirect("catalog:cart_detail")


@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    cart.remove(book)

    return redirect("catalog:cart_detail")


def cart_detail(request):
    cart = Cart(request)

    return render(request, "catalog/cart_detail.html", {
        "cart": cart
    })

def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("catalog:book_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                if request.user.is_authenticated:
                    order.user = request.user

                order.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item["book"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )

                send_mail(
                    subject=f"Замовлення #{order.id} створено",
                    message=f"Ваше замовлення #{order.id} успішно створено.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=True,
                )

                stripe.api_key = settings.STRIPE_SECRET_KEY

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="payment",
                    customer_email=order.email,
                    line_items=[
                        {
                            "price_data": {
                                "currency": "uah",
                                "product_data": {
                                    "name": item["book"].title,
                                },
                                "unit_amount": int(item["price"] * 100),
                            },
                            "quantity": item["quantity"],
                        }
                        for item in cart
                    ],
                    success_url=request.build_absolute_uri(
                        reverse("catalog:payment_success")
                    ),
                    cancel_url=request.build_absolute_uri(
                        reverse("catalog:payment_cancel")
                    ),
                    metadata={
                        "order_id": order.id,
                    },
                )

                order.stripe_session_id = checkout_session.id
                order.save()

                cart.clear()

                return redirect(checkout_session.url)

    else:
        form = OrderCreateForm()

    return render(request, "catalog/order_create.html", {
        "cart": cart,
        "form": form,
    })


def payment_success(request):
    return render(request, "catalog/payment_success.html")


def payment_cancel(request):
    return render(request, "catalog/payment_cancel.html")