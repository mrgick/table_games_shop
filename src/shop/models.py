from io import BytesIO

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
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
    stock = models.PositiveIntegerField(verbose_name="Количество в наличии")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена"
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
    products = models.ManyToManyField(Product, verbose_name="Товары")

    def __str__(self):
        return self.client.username

    class Meta:
        db_table = "Cart"
        verbose_name = "корзина"
        verbose_name_plural = "корзины"


class Order(models.Model):
    class Status(models.IntegerChoices):
        IN_PROCESSING = 0, _("В обработке")
        PENDING = 1, _("Ожидает выдачи")
        COMPLETED = 2, _("Завершён")

    client = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Клиент",
    )
    status = models.PositiveIntegerField(choices=Status.choices, verbose_name="Статус")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Общая сумма"
    )
    products = models.ManyToManyField(Product, verbose_name="Товары")
    date = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name="Дата заказа"
    )

    # TODO: Client first_name, last_name, phone ?

    def __str__(self):
        return f"Заказ #{self.id}"

    class Meta:
        db_table = "Order"
        ordering = ["-date"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"