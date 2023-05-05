from django.contrib import admin
from .models import Payment, Order, OrderedFood


# Register your models here.

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'order_number', 'first_name', 'last_name', 'address', 'city',)
    inlines = [OrderedFoodInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'payment_method', 'amount', 'status', 'created_at',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
