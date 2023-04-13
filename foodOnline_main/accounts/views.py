from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
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
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)
