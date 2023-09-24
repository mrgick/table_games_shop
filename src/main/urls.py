from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("contact/", views.Contact.as_view(), name="contact"),
    path("registration/", views.Registration.as_view(), name="registration"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(
            authentication_form=AuthenticationForm,
            template_name="pages/main/form.html",
            extra_context={
                "title": "Авторизация",
                "action": ".",
                "link": {"name": "Ещё нет аккаунта?", "value": "/registration/"},
                "button": "Войти",
            },
        ),
        name="login",
    ),
]
