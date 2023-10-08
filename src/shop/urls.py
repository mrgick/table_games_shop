from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="product_list"),
    path("<int:category>/", views.ProductList.as_view(), name="product_list"),
    path("product/<int:pk>/", views.ProductDetail.as_view(), name="product_detail"),
]
