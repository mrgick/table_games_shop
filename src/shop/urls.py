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
    path("orders/", views.OrdersList.as_view(), name="orders_list"),
    path("order-delete/<int:pk>/", views.OrderDelete.as_view(), name="order_delete"),
    path("order-edit/<int:pk>/", views.OrderChangeStatus.as_view(), name="order_edit"),
    path("admin-categories/", views.CategoriesAdminList.as_view(), name="admin_categories"),
    path("category/create/", views.CategoryCreate.as_view(), name="category_create"),
    path("category/update/<int:pk>/", views.CategoryUpdate.as_view(), name="category_update"),
    path("category/delete/<int:pk>/", views.CategoryDelete.as_view(), name="category_delete"),
]
