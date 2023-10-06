from django.views.generic import ListView

from .models import Category, Product


class ProductList(ListView):
    template_name = "pages/shop/list.html"
    model = Product

    def get_context_data(self, **kwargs):
        kwargs["categories"] = Category.objects.all()
        kwargs["active_category"] = self.kwargs.get("category")
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        if "category" in self.kwargs:
            return super().get_queryset().filter(category=self.kwargs["category"])
        return super().get_queryset()
