from django.views.generic.base import View, TemplateView
from django.http.response import JsonResponse

class Home(TemplateView):
    """ Class for home page. """
    template_name = "pages/index.html"
