import json
from django.db import models
from unicodedata import decimal

from accounts.models import User, UserProfile
from menu.models import FoodItem

from vendor.models import Vendor

# Create your models here.

request_object = None


class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_data = models.JSONField(blank=True, null=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def order_placed_to(self):
        x = ",".join([str(i) for i in self.vendors.all()])
        print('Hejkaaaaaaaaaa')
        print(x)
        return x

    # wybieramy danego vendora
    def get_total_price_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        dict_total_order_data = json.loads(self.total_data)
        total_price_vendor = 0
        # print(dict_total_order_data[f'{vendor.id}'])
        for food in dict_total_order_data[f'{vendor.id}']:
            total_price_vendor += dict_total_order_data[f'{vendor.id}'][food]['total_price']
        print("Total price =", total_price_vendor)
        return total_price_vendor

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ordered food'
        verbose_name_plural = 'ordered food'

    def __str__(self):
        return self.fooditem.food_title
