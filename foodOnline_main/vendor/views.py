from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.contrib import messages
from accounts.views import check_role_vendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from orders.models import Order, OrderedFood
from vendor.models import Vendor


# Create your views here.

def vprofile(request):
    return render(request, 'vendor/vprofile.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)  # pobieranie obiekty (z bazy danych) ktory ma dane requrst.user
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    food = FoodItem.objects.filter(vendor=vendor)
    context = {
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = Category.objects.get(pk=pk)
    foodItems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'foodItems': foodItems
    }
    print(foodItems)
    return render(request, 'vendor/fooditems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form.save()  # save to database
            messages.success(request, "Category has been added")
            return redirect('menu_builder')
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


"""
retrieves an object of the Category model from the database with the primary key (pk) specified in the pk variable. 
If the object is found, the function returns the object and assigns it to the category variable. 
If the object is not found, get_object_or_404 raises a Http404 exception, which results in the display of a 404 error page to the user."""


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)  # podmienienie z instance=category na request.POST
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.slug = slugify(category_name)
            form.save()  # save to database
            messages.success(request, "Category has been added")
            return redirect('menu_builder')
    else:
        form = CategoryForm(
            instance=category)  # tworzenie nowej instancji Cateogry form i przekazywanie jej danych z instancji category
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)  # request.FILES - photo
        if form.is_valid():
            food_name = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            food.slug = slugify(food_name)
            form.save()  # save to database
            messages.success(request, "Food has been added")
            return redirect('fooditems_by_category',
                            food.category.id)  # 'menu-builder/category/<int:pk>/' , <int:pk> = food.category.id
            # return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=Vendor.objects.get(
            user=request.user))  # zeby nie pobieraly sie wszystkie kategorie jedzenia tylko katergorie jedzenia danego sprzedacwy
        context = {
            'form': form,
        }
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    print(food)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES,
                            instance=food)  # podmienienie z instance=category na request.POST
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            food.slug = slugify(foodtitle)
            form.save()  # save to database
            messages.success(request, "Food item has been added")
            return redirect('fooditems_by_category',
                            food.category.id)  # 'menu-builder/category/<int:pk>/' , <int:pk> = food.category.id
        else:
            print(form.errors)
    else:
        form = FoodItemForm(
            instance=food)  # tworzenie nowej instancji Cateogry form i przekazywanie jej danych z instancji category
        form.fields['category'].queryset = Category.objects.filter(vendor=Vendor.objects.get(
            user=request.user))  # zeby nie pobieraly sie wszystkie kategorie jedzenia tylko katergorie jedzenia danego sprzedacwy

    print(form)
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food has been deleted')
    return redirect('fooditems_by_category', food.category.id)


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=Vendor.objects.get(user=request.user))

        total_price = 0
        for food in ordered_food:
            total_price += food.price * food.quantity

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'total_price': total_price,
        }
        return render(request, 'vendor/order_detail.html', context)
    except:
        return redirect('vendor')
