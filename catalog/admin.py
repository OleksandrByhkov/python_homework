from django.contrib import admin
from .models import Book, Category, Order, OrderItem

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "price", "stock")
    list_filter = ("category", "author")
    search_fields = ("title", "author", "description")
    list_editable = ("price", "stock")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "paid",
        "status",
        "created_at",
    )
    list_filter = ("paid", "status", "created_at")
    search_fields = ("email", "first_name", "last_name")
    inlines = [OrderItemInline]