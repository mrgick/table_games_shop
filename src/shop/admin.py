from django.contrib import admin

from .models import Cart, CartItem, Category, Order, OrderItem, Product

admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "stock")
    search_fields = ("title",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "date", "status")
    list_filter = ("client", "status")
    search_fields = ("client", )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order","product","quantity","total")
    list_filter = ("order",)
