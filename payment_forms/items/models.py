from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название товара",
        help_text="Укажите название товара",
    )
    description = models.TextField(
        verbose_name="Текстовое описание",
        help_text="Введите текстовое описание",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена товара",
        help_text="Укажите цену товара",
        default=0,
    )

    def __str__(self):
        return self.name
