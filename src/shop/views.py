import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from .models import Cart, CartItem, Category, Product, Order, OrderItem


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
            return redirect('cart_detail')
        order = Order(client=request.user, status=0, count=cart.count, total=cart.total)
        order.save()
        for cart_item in CartItem.objects.filter(cart=cart):
            order_item = OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity, total=cart_item.total)
            order_item.calculate()
            order_item.save()
        order.calculate()
        order.save()
        cart.delete()
        cart = Cart(client=request.user)
        cart.save()
        return JsonResponse({1:1})