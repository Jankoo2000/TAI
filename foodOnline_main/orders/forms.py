from django import forms

from orders.models import Order
from marketplace.models import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'city', 'pin_code']
