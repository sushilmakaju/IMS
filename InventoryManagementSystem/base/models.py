from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

usertype_list = [('Buyer', 'Buyer'), ('Seller', 'Seller')]
Producttype_list = [('Electronics', 'Electronics') , ('Clothes', 'Clothes')]
order_status = [('Pending' , 'Pending'), ('Delivered' , 'Delivered')]
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200, default='User')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    user_type = models.CharField(max_length=50, choices=usertype_list)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Seller(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    phone_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Buyer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    age = models.IntegerField()
    phone_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=Producttype_list)
    stock = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices= order_status)  
    total_amount = models.IntegerField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()

