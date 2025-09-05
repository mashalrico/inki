# app/admin.py
from django.contrib import admin
from .models import Product , PageVisit

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "followers_count", "category", "product_number")
    search_fields = ("name", "category", "product_number", "color")
    list_filter = ("category",)
@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ("path", "ip_address", "session_key", "timestamp")
    search_fields = ("path", "ip_address", "session_key")
    list_filter = ("timestamp",)