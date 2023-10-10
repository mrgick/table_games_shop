import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.views.generic import DetailView, ListView, View

from .models import Cart, CartItem, Category, Product


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
        queryset = super().get_queryset().filter(stock__gte=0)
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
    def put(self, request: HttpRequest):
        """Update product in cart"""
        cart = Cart.objects.filter(client=request.user).first()
        if cart is None:
            cart = Cart(client=request.user)
            cart.save()
        body = json.loads(request.body)
        product = Product.objects.get(pk=body["product_id"])
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item is None:
            cart_item = CartItem(
                cart=cart,
                product=product,
            )
        if body["quantity"] <= 0:
            if cart_item.quantity:
                cart_item.delete()
            return JsonResponse({"product_id": product.id, "quantity": 0})
        if body["quantity"] > product.stock:
            body["quantity"] = product.stock
        cart_item.quantity = body["quantity"]
        cart_item.save()
        return JsonResponse(
            {"product_id": cart_item.product.id, "quantity": cart_item.quantity}
        )
