from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from catalog.models import Book


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone",
            "address",
            "password1",
            "password2",
        ]

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "price", "stock", "category"]

        labels = {
            "title": _("Title"),
            "author": _("Author"),
            "description": _("Description"),
            "price": _("Price"),
            "stock": _("Stock"),
            "category": _("Category"),
        }