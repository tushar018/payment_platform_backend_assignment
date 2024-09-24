from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, PaymentLink


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(PaymentLink)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)

