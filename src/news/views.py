from django.views.generic import DetailView, ListView

from .forms import CommentForm
from .models import Comment, News


class NewsList(ListView):
    template_name = "pages/news/list.html"
    model = News


class NewsDetail(DetailView):
    template_name = "pages/news/detail.html"
    model = News

    def get_context_data(self, **kwargs):
        kwargs["comments"] = Comment.objects.filter(news=kwargs["object"].id)
        kwargs["form"] = CommentForm()
        return super().get_context_data(**kwargs)


# class CreateNews(FormView):
#     """Class for the registration."""

#     template_name = "pages/main/form.html"
#     # form_class = UserCreationForm
#     success_url = "/"

#     def form_valid(self, form):
#         news = form.save(commit=False)
#         news.author = self.request.user
#         news.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         kwargs["title"] = "Создать новость"
#         kwargs["action"] = "."
#         kwargs["button"] = "Создать"
#         return super().get_context_data(**kwargs)
