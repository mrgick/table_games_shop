from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, NewsForm
from .models import Comment, News


class NewsList(ListView):
    template_name = "pages/news/list.html"
    model = News


class NewsDetail(DetailView):
    template_name = "pages/news/detail.html"
    model = News

    def get_context_data(self, **kwargs):
        kwargs["comments"] = Comment.objects.filter(news=kwargs["object"].id)
        if self.request.user.is_authenticated:
            kwargs["form"] = CommentForm()
        return super().get_context_data(**kwargs)

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if request.user.is_authenticated and form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news = News.objects.get(id=pk)
            comment.save()
            return redirect(f'{reverse("news_detail", args=[pk])}#{comment.id}')
        return redirect("news_detail", pk=pk)


class NewsCreate(CreateView):
    """Class for the create/edit news."""

    template_name = "pages/main/form.html"
    form_class = NewsForm
    success_url = "/news/"
    # TODO: perms

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = self.request.user
        news.save()
        return redirect("news_detail", pk=news.id)

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Создание новости"
        kwargs["action"] = "."
        kwargs["button"] = "Создать"
        kwargs["link"] = {"name": "Назад к новостям", "value": reverse("news_list")}
        return super().get_context_data(**kwargs)


class NewsEdit(UpdateView):
    """Class for the create/edit news."""

    template_name = "pages/main/form.html"
    form_class = NewsForm
    model = News
    success_url = "/news/"
    # TODO: perms

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = self.request.user
        news.save()
        return redirect("news_detail", pk=news.id)

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Редактирование новости"
        kwargs["action"] = "."
        kwargs["button"] = "Сохранить"
        kwargs["link"] = {
            "name": "Назад к новости",
            "value": reverse("news_detail", args=[self.object.id]),
        }
        return super().get_context_data(**kwargs)


class NewsDelete(DeleteView):
    """Class for the create/edit news."""

    template_name = "pages/main/form.html"
    # form_class = NewsForm
    model = News
    success_url = "/news/"

    # TODO: perms
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            {
                "title": f"Удаление новости c id={self.object.id} и именем '{self.object}'",
                "action": ".",
                "button": "Удалить",
                "link": {
                    "name": "Назад к новости",
                    "value": reverse("news_detail", args=[self.object.id]),
                },
            }
        )
        return super().get_context_data(**kwargs)
