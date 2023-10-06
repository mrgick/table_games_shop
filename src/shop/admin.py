from django.contrib import admin

from .models import Cart, Category, Order, Product

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
