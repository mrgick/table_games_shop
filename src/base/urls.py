from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view()),
    path("contact/", views.Contact.as_view(), name="contact"),
]
