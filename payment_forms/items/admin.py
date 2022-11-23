from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"
