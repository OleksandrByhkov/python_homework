from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["title"]
        permissions = [
            ("can_manage_books", "Can manage books"),
        ]

    def __str__(self):
        return f"{self.title} — {self.author}"