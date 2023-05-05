from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from accounts.models import UserProfile
from marketplace.context_processors import get_cart_amounts
from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, Payment, OrderedFood
from orders.utils import generate_order_id


# Create your views here.


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = Order()
            order.user = request.user
            order.order_number = generate_order_id()
            order.first_name = order_form.cleaned_data['first_name']
            order.last_name = order_form.cleaned_data['last_name']
            order.phone = order_form.cleaned_data['phone']
            order.email = order_form.cleaned_data['email']
            order.address = order_form.cleaned_data['address']
            order.city = order_form.cleaned_data['city']
            order.country = order_form.cleaned_data['country']
            order.pin_code = order_form.cleaned_data['pin_code']
            order.total = get_cart_amounts(request)['total_price']

            order.save()
            context = {
                'order': order,
            }
            print(order)
            messages.success(request, 'Saved to database')
            return render(request, 'marketplace/place_order.html', context)

        else:
            print(order_form.errors)
            messages.success(request, 'Error')
    else:
        print('------------44-------------')
        user_profile = UserProfile.objects.get(user=request.user)
        default_values = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone_number,
            'email': request.user.email,
            'address': user_profile.address_line_1,
            'country': user_profile.country,
            'city': user_profile.city,

        }

        order_form = OrderForm(initial=default_values)

    context = {
        'order_form': order_form
    }
    return render(request, 'marketplace/checkout.html', context)


def place_order(request):
    return render(request, 'marketplace/place_order.html')


"""

    data : {
        'order_number' : order_number,
        'transaction_id' : transaction_id,
        'payment_metod' : payment_method,
        'status' : status,
        'csfrmiddlewaretoken' : csfrtoken,
    },
"""


def payments(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST'):
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        print(order_number, transaction_id, payment_method, status)

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            status=status,
            amount=order.total
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity
            ordered_food.save()

        # clear the cart if the payment is success
        cart_items.delete()

        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)

    return HttpResponse('Hejka co sie tam z toba dzieje skad to zwatpienie')


def order_complete(request):
    print('--------- hejka tu lenka -------------')
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    print('---data----')
    print(order_number)
    print(transaction_id)

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)

        context = {
            'order': order,
            'ordered_food': ordered_food,
        }
        return render(request, 'marketplace/order_complete.html', context)

    except:
        return redirect('home')

