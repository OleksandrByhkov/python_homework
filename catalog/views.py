from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, Category


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