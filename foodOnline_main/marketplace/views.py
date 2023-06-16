from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from accounts.models import UserProfile
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from orders.forms import OrderForm
from marketplace.models import Cart
from menu.models import Category, FoodItem
from orders.models import Order
from vendor.models import Vendor


# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug=None):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


"""
Json are to comunicate with javascritp
"""


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase the cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Sucess', 'message': 'Increased the cart quantity',
                                         'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the product to cart',
                                         'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)
                                         })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'This file does not exist'})

    return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # decrease the cart quantity
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0

                    return JsonResponse({'status': 'Sucess', 'message': 'Increased the cart quantity',
                                         'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})  # 108

                except:
                    print('----------------------------------------')
                    return JsonResponse({'status': 'Failed', 'message': 'You dont have this product in your cart',
                                         'qty': checkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})  ## wywala warunek
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'This file does not exist'})

    return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


# not finisihed and not required
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Sucess', 'message': 'Cart item has been deleted'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in'})
