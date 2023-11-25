from decimal import Decimal
from io import BytesIO

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Category"
        ordering = ["-id"]
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Изображение")
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
    )
    stock = models.BooleanField(default=True, verbose_name="В наличии")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Цена",
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    def compress_logo(self, image):
        im = Image.open(image)
        im_bytes = BytesIO()
        im.save(fp=im_bytes, format="WEBP", quality=100)
        image_content_file = ContentFile(content=im_bytes.getvalue())
        name = image.name.split(".")[0] + ".WEBP"
        new_image = File(image_content_file, name=name)
        return new_image

    def save(self, *args, **kwargs):
        try:
            object = Product.objects.filter(id=self.id).first()
            if object and object.image != self.image:
                self.image = self.compress_logo(self.image)
                object.image.delete(save=False)
        except ValueError:
            pass
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Product"
        ordering = ["-id"]
        verbose_name = "товар"
        verbose_name_plural = "товары"


class Cart(models.Model):
    client = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
    )
    count = models.PositiveIntegerField(default=0, verbose_name="Количество товаров")
    total = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость"
    )
    items = models.ManyToManyField(
        Product, through="CartItem", through_fields=("cart", "product")
    )

    def save(self, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart=self.id)
        self.count = sum(x.quantity for x in cart_items)
        self.total = sum(x.total for x in cart_items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Корзина клиента {self.client.username}"

    class Meta:
        db_table = "Cart"
        verbose_name = "корзина"
        verbose_name_plural = "корзины"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, verbose_name="Общая сумма"
    )

    def clean(self):
        if not self.product.stock:
            raise ValidationError({"quantity": "Товар должен быть в наличии."})

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.product.price
        super().save(*args, **kwargs)
        self.cart.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.save()

    def __str__(self):
        return f"{self.product.title} ({self.quantity} шт.) в корзине {self.cart.client.username}"

    class Meta:
        db_table = "Cart_item"
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"


class Order(models.Model):
    class Status(models.IntegerChoices):
        PROCESSING = 0, _("В обработке")
        PENDING = 1, _("Ожидает выдачи")
        COMPLETED = 2, _("Завершён")

    client = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Клиент",
    )
    status = models.PositiveIntegerField(choices=Status.choices, verbose_name="Статус")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество товаров")
    total = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость"
    )
    date = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name="Дата заказа"
    )
    items = models.ManyToManyField(
        Product, through="OrderItem", through_fields=("order", "product")
    )

    def calculate(self):
        items = OrderItem.objects.filter(order=self.id)
        self.count = sum(x.quantity for x in items)
        self.total = sum(x.total for x in items)
        self.save()

    def __str__(self):
        return f"Заказ #{self.id}"

    class Meta:
        db_table = "Order"
        ordering = ["-date"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, verbose_name="Товар"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2, verbose_name="Общая сумма"
    )

    def __str__(self):
        return f"{self.product.title} ({self.quantity} шт.) в заказе #{self.order.id}"

    def calculate(self, *args, **kwargs):
        self.total = self.quantity * self.product.price
        self.save()

    class Meta:
        db_table = "Order_item"
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"
