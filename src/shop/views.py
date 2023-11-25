import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Cart, CartItem, Category, Order, OrderItem, Product


class ProductList(ListView):
    template_name = "pages/shop/list.html"
    model = Product

    def get_context_data(self, **kwargs):
        kwargs["categories"] = Category.objects.all()
        kwargs["active_category"] = self.kwargs.get("category")
        kwargs["products_in_cart"] = set()
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(client=self.request.user).first()
            if cart is not None:
                kwargs["products_in_cart"] = {
                    x["product"]
                    for x in CartItem.objects.filter(cart=cart).values("product")
                }
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(stock=True)
        if "category" in self.kwargs:
            return queryset.filter(category=self.kwargs["category"])
        return queryset


class ProductDetail(DetailView):
    template_name = "pages/shop/detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        kwargs["product_in_cart"] = False
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(client=self.request.user).first()
            if cart is not None:
                kwargs["product_in_cart"] = CartItem.objects.filter(
                    cart=cart, product=self.object.id
                ).exists()
        return super().get_context_data(**kwargs)


class CartUpdate(LoginRequiredMixin, View):
    def update_cart_item(self, user, product_id, quantity):
        """Update product in cart"""
        cart = Cart.objects.filter(client=user).first()
        if cart is None:
            cart = Cart(client=user)
            cart.save()
        product = Product.objects.get(pk=product_id)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item is None:
            cart_item = CartItem(
                cart=cart,
                product=product,
            )
        if not product.stock or quantity <= 0:
            cart_item.delete()
            return cart_item
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def put(self, request: HttpRequest):
        """Update product in cart"""
        body = json.loads(request.body)
        cart_item = self.update_cart_item(
            request.user, body["product_id"], body["quantity"]
        )
        return JsonResponse(
            {"product_id": cart_item.product.id, "quantity": cart_item.quantity}
        )

    def post(self, request: HttpRequest, product_id, quantity):
        """Update product in cart (browser)"""
        self.update_cart_item(request.user, product_id, quantity)
        return redirect("cart_detail")


class CartDetail(LoginRequiredMixin, DetailView):
    template_name = "pages/shop/cart.html"
    model = Cart

    def get_object(self, queryset=None):
        cart = Cart.objects.filter(client=self.request.user).first()
        if cart is None:
            cart = Cart(client=self.request.user)
            cart.save()
        return cart

    def get_context_data(self, **kwargs):
        kwargs["cart_items"] = CartItem.objects.filter(cart=self.object)
        return super().get_context_data(**kwargs)

    def post(self, request):
        """Create order"""
        cart = Cart.objects.filter(client=request.user).first()
        if cart is None or cart.count == 0:
            return redirect("cart_detail")
        order = Order(client=request.user, status=0, count=cart.count, total=cart.total)
        order.save()
        for cart_item in CartItem.objects.filter(cart=cart):
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                total=cart_item.total,
            )
            order_item.calculate()
            order_item.save()
        order.calculate()
        order.save()
        cart.delete()
        cart = Cart(client=request.user)
        cart.save()
        return redirect("orders_list")


class OrdersList(LoginRequiredMixin, ListView):
    template_name = "pages/shop/orders.html"
    model = Order

    def get_queryset(self):
        if self.request.user.is_staff:
            return (
                Order.objects.order_by("-date")
                .prefetch_related("items__orderitem_set")
                .all()
            )
        return (
            Order.objects.order_by("-date")
            .filter(client=self.request.user)
            .prefetch_related("items__orderitem_set")
            .all()
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.user.is_superuser:
            kwargs["active_url"] = "Заказы"
        return super().get_context_data(**kwargs)


class OrderDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = "pages/main/form.html"
    permission_required = "orders.delete_order"
    order = Order

    success_url = "/shop/orders/"

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        kwargs["title"] = f"Удаление заказа #{self.object.id}"
        kwargs["action"] = "."
        kwargs["button"] = "Удалить"
        kwargs["link"] = {
            "name": "Назад к заказам",
            "value": "/shop/orders/",
        }
        return super().get_context_data(**kwargs)


class OrderChangeStatus(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "pages/main/form.html"
    permission_required = "orders.change_order"
    order = Order
    fields = ["status", "client"]
    success_url = "/shop/orders/"

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        kwargs["title"] = f"Изменение заказа #{self.object.id}"
        kwargs["action"] = "."
        kwargs["button"] = "Сохранить"
        kwargs["link"] = {
            "name": "Назад к заказам",
            "value": "/shop/orders/",
        }
        return super().get_context_data(**kwargs)


class CategoryCreate(PermissionRequiredMixin, CreateView):
    template_name = "pages/main/form.html"
    success_url = "/shop/admin-categories/"
    fields = "__all__"
    model = Category
    permission_required = "category.add_category"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Создание категории"
        kwargs["action"] = "."
        kwargs["button"] = "Создать"
        kwargs["link"] = {
            "name": "Назад в панель",
            "value": reverse("admin_categories"),
        }
        return super().get_context_data(**kwargs)


class CategoryUpdate(PermissionRequiredMixin, UpdateView):
    template_name = "pages/main/form.html"
    model = Category
    fields = "__all__"
    success_url = "/shop/admin-categories/"
    permission_required = "category.change_category"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Редактирование категории"
        kwargs["action"] = "."
        kwargs["button"] = "Сохранить"
        kwargs["link"] = {
            "name": "Назад в панель",
            "value": reverse("admin_categories"),
        }
        return super().get_context_data(**kwargs)


class CategoryDelete(PermissionRequiredMixin, DeleteView):
    template_name = "pages/main/form.html"
    model = Category
    success_url = "/shop/admin-categories/"
    permission_required = "category.delete_category"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            {
                "title": f"Удаление категории #{self.object.id} {self.object}",
                "action": ".",
                "button": "Удалить",
                "link": {
                    "name": "Назад в панель",
                    "value": reverse("admin_categories"),
                },
            }
        )
        return super().get_context_data(**kwargs)


class CategoriesAdminList(PermissionRequiredMixin, ListView):
    template_name = "pages/main/admin_panel.html"
    model = Category
    permission_required = ["category.view_category"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.update(
            {
                "active_url": "Категории",
                "url_id": "product_list",
                "url_edit": "category_update",
                "url_delete": "category_delete",
                "url_create": "category_create",
            }
        )
        return super().get_context_data(**kwargs)


class ProductCreate(PermissionRequiredMixin, CreateView):
    template_name = "pages/main/form.html"
    success_url = "/shop/admin-products/"
    fields = "__all__"
    model = Product
    permission_required = "product.add_product"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Создание товара"
        kwargs["action"] = "."
        kwargs["button"] = "Создать"
        kwargs["link"] = {
            "name": "Назад в панель",
            "value": reverse("admin_products"),
        }
        return super().get_context_data(**kwargs)


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    template_name = "pages/main/form.html"
    model = Product
    fields = "__all__"
    success_url = "/shop/admin-products/"
    permission_required = "product.change_product"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Редактирование товара"
        kwargs["action"] = "."
        kwargs["button"] = "Сохранить"
        kwargs["link"] = {
            "name": "Назад в панель",
            "value": reverse("admin_products"),
        }
        return super().get_context_data(**kwargs)


class ProductDelete(PermissionRequiredMixin, DeleteView):
    template_name = "pages/main/form.html"
    model = Product
    success_url = "/shop/admin-products/"
    permission_required = "product.delete_product"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            {
                "title": f"Удаление товара #{self.object.id} {self.object}",
                "action": ".",
                "button": "Удалить",
                "link": {
                    "name": "Назад в панель",
                    "value": reverse("admin_products"),
                },
            }
        )
        return super().get_context_data(**kwargs)


class ProducsAdminList(PermissionRequiredMixin, ListView):
    template_name = "pages/main/admin_panel.html"
    model = Product
    permission_required = ["product.view_product"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.update(
            {
                "active_url": "Товары",
                "url_id": "product_detail",
                "url_edit": "product_update",
                "url_delete": "product_delete",
                "url_create": "product_create",
            }
        )
        return super().get_context_data(**kwargs)
