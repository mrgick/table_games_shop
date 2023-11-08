from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="product_list"),
    path("<int:category>/", views.ProductList.as_view(), name="product_list"),
    path("product/<int:pk>/", views.ProductDetail.as_view(), name="product_detail"),
    path("cart-update/", views.CartUpdate.as_view(), name="cart_update"),
    path("cart/", views.CartDetail.as_view(), name="cart_detail"),
    path(
        "cart-update/<int:product_id>/<int:quantity>/",
        views.CartUpdate.as_view(),
        name="cart_update",
    ),
    path("orders/", views.OrdersList.as_view(), name="orders_list")
]
