from django.db.models import Q, Count
from .models import Book, Category

cheap_books = Book.objects.filter(price__lt=500)

available_books = Book.objects.filter(stock__gt=0)

search_books = Book.objects.filter(
    Q(author__icontains="Shevchenko") | Q(author__icontains="Franko")
)

price_and_stock = Book.objects.filter(
    Q(price__lt=1000) & Q(stock__gt=0)
)

cat_with_book_count = Category.objects.annotate(
    books_count=Count("books")
)

for category in cat_with_book_count:
    print(category.name, category.books_count)