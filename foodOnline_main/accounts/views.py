from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm

def registerUser(request):
    if request.method == 'POST':
        #print(request.POST)
        form = UserForm(request.POST) # reqest.POST dict with data from registerUser saved into form
        if form.is_valid(): # method is used to perform validation for each field of the form, it is defined in Django Form class. It returns True if data is valid and place all data into a cleaned_data attribute
            password = form.cleaned_data['password'] # cleaned_data conversion to dic
            user = form.save(commit=False) # The commit=False argument to save() tells Django not to save the object to the database yet. This allows you to add any additional fields to the object before saving it to the database.
            user.set_password(password) # hashing password (neccecary in admin panel)
            user.role = User.CUSTOMER
            user.save() ## saving to database
            messages.error(request, 'Your account has been registered sucessfully')
            return redirect('registerUser') ## redirects to given url (e.x https://www.sport.pl)
        else:
            print('invalid form')
            print(form.errors) ## bulid in uniqeue username and checker
    else:
        form = UserForm() #
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    # POST, GET, PUT, DELETE
    # button register is type submit to it's POST function
    if request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST) # request.POST w Django to słownik, który zawiera dane przesłane przez użytkownika do serwera za pomocą metody HTTP POST po kliknieciu przecisku typu submit.
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            print('0')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name, last_name, username, email, password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False) # vendor only with vendor_name and vendor_license
            vendor.user = user # OneToOneFiled
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile # OneToOneFiled
            print(vendor)
            vendor.save()
            messages.success(request, 'Your account has been registred sucessfully! Please wait for the approval')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        # generate forms and print html
        form = UserForm()
        v_form = VendorForm()
        context = {
            'form' : form,
            'v_form' : v_form
        }
        return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password) #  funkcja authenticate() jest użyta do uwierzytelnienia użytkownika na podstawie przesłanych przez niego danych logowania (nazwa użytkownika i hasło
        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

