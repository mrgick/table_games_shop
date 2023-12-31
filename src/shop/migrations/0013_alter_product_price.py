# Generated by Django 4.2.5 on 2023-11-25 16:42

from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0012_cart_items_alter_orderitem_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                verbose_name="Цена",
            ),
        ),
    ]
