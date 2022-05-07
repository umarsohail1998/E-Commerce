from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.enums import Choices
from django.db.models.fields import CharField


class ContactUs(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    phone=models.IntegerField()
    message=models.CharField(max_length=200)

STATE_CHOICES = (
    ('KPK', 'KPK'),
    ('Sindh', 'Sindh'),
    ('Punjab', 'Punjab'),
    ('Balochistan', 'Balochistan'),
    ('Gilgit Baltistan ', 'Gilgit Baltistan'),
    ('Jammu and kashmir', 'Jammu and kashmir '),

)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50)


    def __str__(self):
        return self.name

CATEGORY_CHOICES = (
    ('C', 'cookware'),
    ('E', 'electronics'),
    ('D', 'dinning'),
    ('k', 'kitchentools'),)

class Product(models.Model):
    tittle = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    discription = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=4)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.tittle

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)
    
    
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    total_price=property(total_cost)

STATUS_CHOICES = (
    ('accepted', 'accepted'),
    ('packed', 'packed'),
    ('on_the_way ', 'on_the_way'),
    ('delevered', 'delevered'),
    ('cancel', 'cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='pending')
    total_price=models.CharField(max_length=10)
    
