from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


class Home(TemplateView):
    """Class for home page."""

    template_name = "pages/main/index.html"


class Contact(TemplateView):
    """Class for contacts page."""

    template_name = "pages/main/contact.html"


class Registration(FormView):
    """Class for the registration."""

    template_name = "pages/main/form.html"
    form_class = UserCreationForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.date_joined = timezone.now()
        user.last_login = timezone.now()
        user.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Регистрация"
        kwargs["action"] = "."
        kwargs["button"] = "Зарегистрироваться"
        kwargs["link"] = {"name": "Уже есть аккаунт?", "value": "login"}
        return super().get_context_data(**kwargs)
