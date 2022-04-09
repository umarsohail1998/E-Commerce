from django.contrib import admin
from django.db import models
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    ContactUs
)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'email',
                    'phone', 'message']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'locality', 'city', 'zipcode', 'state']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittle', 'selling_price', 'discounted_price',
                    'discription', 'brand', 'category', 'product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product',
                    'quantity','total_price']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer',
                    'product', 'quantity', 'ordered_date', 'status','total_price']
