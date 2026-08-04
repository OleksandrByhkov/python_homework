from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Book, Category


def invalidate_book_list_cache():
    """
    Clear cached book-list pages.

    Redis backend supports deleting keys by exact name only through
    Django's standard cache API, so the cache version is incremented
    by clearing the configured cache.
    """
    cache.clear()


@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    """Invalidate book detail and book-list caches."""

    cache.delete(f"book_detail:{instance.pk}")
    invalidate_book_list_cache()


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    """Invalidate book-list caches after category changes."""

    invalidate_book_list_cache()