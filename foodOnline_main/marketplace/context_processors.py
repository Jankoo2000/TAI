from .models import Cart
from menu.models import FoodItem

"""
A function defined in a context processor in Django 
is executed for every request that is processed by the Django application (in this case marketplace application). (probably not only)
This means that the function is called every time some url or function from this app is used, 
regardless of which view function is handling the request.
Funtions must return dict
"""
def get_cart_counter(request):

    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0

        except:
            cart_count = 0

    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    total_price = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            total_price += (fooditem.price * item.quantity)
    x = dict(total_price=total_price)
    # print(x)
    return dict(total_price=total_price)
