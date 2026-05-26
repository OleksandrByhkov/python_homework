from django.db.models import Q, Count
from .models import Book, Category


def show_orm_examples():
    print("=== Книги дешевші за 500 ===")
    cheap_books = Book.objects.filter(price__lt=500)

    for book in cheap_books:
        print(f"{book.title} | {book.author} | {book.price} грн")

    print("\n=== Книги, які є на складі ===")
    available_books = Book.objects.filter(stock__gt=0)

    for book in available_books:
        print(f"{book.title} | залишок: {book.stock}")

    print("\n=== Книги авторів Shevchenko або Franko ===")
    search_books = Book.objects.filter(
        Q(author__icontains="Shevchenko") |
        Q(author__icontains="Franko")
    )

    for book in search_books:
        print(f"{book.title} | автор: {book.author}")

    print("\n=== Книги дешевші за 1000 і є на складі ===")
    price_and_stock = Book.objects.filter(
        Q(price__lt=1000) &
        Q(stock__gt=0)
    )

    for book in price_and_stock:
        print(f"{book.title} | {book.price} грн | залишок: {book.stock}")

    print("\n=== Кількість книг у кожній категорії ===")
    categories_with_count = Category.objects.annotate(
        books_count=Count("books")
    )

    for category in categories_with_count:
        print(f"{category.name}: {category.books_count} книг")