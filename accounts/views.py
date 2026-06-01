from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("catalog:book_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    pass
