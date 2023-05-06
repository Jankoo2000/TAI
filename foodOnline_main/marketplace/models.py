from django.db import models

from accounts.models import User
from menu.models import FoodItem


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # date is unchangeable
    updated_at = models.DateTimeField(auto_now=True)  # when object is modyfied date will be changed

    def __unicode__(self):
        return self.user
