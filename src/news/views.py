from django.views.generic import DetailView, ListView

from .models import News


class NewsList(ListView):
    template_name = "app/blog.html"
    model = News


class NewsDetail(DetailView):
    template_name = "app/blog.html"
    model = News


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
