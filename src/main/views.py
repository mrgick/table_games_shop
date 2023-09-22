from django.views.generic.base import View, TemplateView
from django.http.response import JsonResponse

class Home(TemplateView):
    """ Class for home page. """
    template_name = "pages/index.html"

class Contact(TemplateView):
    """ Class for contacts page. """
    template_name = "pages/contact.html"
