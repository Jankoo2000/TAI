from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
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
    print('-----registerVendor-----------')
    if request.method == 'POST':
        # store the data and create the user
        print('NNNNNNNN------NNNNNNN')
        form = UserForm(request.POST) # request.POST w Django to słownik, który zawiera dane przesłane przez użytkownika do serwera za pomocą metody HTTP POST po kliknieciu przecisku typu submit.
        print('NNNNNNNN+++++++NNNNNNN')
        v_form = VendorForm(request.POST, request.FILES)
        print('MMMMMMMMMMMMMMM')
        if form.is_valid() and v_form.is_valid():
            print('0')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name, last_name, username, email, password)
            print('1')
            user.role = User.VENDOR
            user.save()
            print('2')
            vendor = v_form.save(commit=False) # vendor only with vendor_name and vendor_license
            print('3')
            vendor.user = user # OneToOneFiled
            print('4')
            user_profile = UserProfile.objects.get(user=user)
            print('5')
            vendor.user_profile = user_profile # OneToOneFiled
            print('6')
            print(vendor)
            vendor.save()
            print('7')
            messages.success(request, 'Your account has been registred sucessfully! Please wait for the approval')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        print('$$$$$$$$$registerVendor$$$$$$$$$$$$$')

        # generate forms and print html
        form = UserForm()
        v_form = VendorForm()
        context = {
            'form' : form,
            'v_form' : v_form
        }
        print('yolo')
        return render(request, 'accounts/registerVendor.html', context)
