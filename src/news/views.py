from typing import Any
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import News


class NewsList(ListView):
    template_name = "pages/news/list.html"
    model = News


class NewsDetail(DetailView):
    template_name = "pages/news/detail.html"
    model = News


class NewsCreate(PermissionRequiredMixin, CreateView):
    """Class for the create/edit news."""

    template_name = "pages/main/form.html"
    success_url = "/news/admin-news/"
    fields = "__all__"
    model = News
    permission_required = "news.add_news"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Создание новости"
        kwargs["action"] = "."
        kwargs["button"] = "Создать"
        kwargs["link"] = {
            "name": "Назад в панель",
            "value": reverse("admin_news"),
        }
        return super().get_context_data(**kwargs)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    """Class for the create/edit news."""

    template_name = "pages/main/form.html"
    model = News
    fields = "__all__"
    success_url = "/news/admin-news/"
    permission_required = "news.change_news"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Редактирование новости"
        kwargs["action"] = "."
        kwargs["button"] = "Сохранить"
        kwargs["link"] = {
            "name": "Назад в панель",
            "value": reverse("admin_news"),
        }
        return super().get_context_data(**kwargs)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    """Class for the create/edit news."""

    template_name = "pages/main/form.html"
    model = News
    success_url = "/news/admin-news/"
    permission_required = "news.delete_news"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            {
                "title": f'Удаление новости #{self.object.id} {self.object}',
                "action": ".",
                "button": "Удалить",
                "link": {
                    "name": "Назад в панель",
                    "value": reverse("admin_news"),
                },
            }
        )
        return super().get_context_data(**kwargs)


class NewsAdminList(PermissionRequiredMixin, ListView):
    template_name = "pages/main/admin_panel.html"
    model = News
    permission_required = ["news.view_news"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.update({
            "active_url":"Новости",
            "url_id": "news_detail",
            "url_edit":"news_edit",
            "url_delete":"news_delete",
            "url_create": "news_create"
        })
        return super().get_context_data(**kwargs)