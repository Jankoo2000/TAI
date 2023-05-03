from django import forms
from .models import User, UserProfile

"""
Formularz class Metaw Django to sposób na określenie metadanych dotyczących formularza, takich jak model, 
z którym formularz jest powiązany, pola do uwzględnienia lub wykluczenia w formularzu oraz wszelkie dodatkowe opcje, które powinny być użyte podczas renderowania formularza
Generujemy formularze z klasy meta bo nie chcemy zeby wszystkie pola byly w tym formularzu


W tym przypadku określamy, że formularz jest powiązany z User 
i że chcemy uwzględnić tylko pola 'first_name', 'last_name', 'username', 'email', 'phone_number'] 
z modelu User oraz dodac pole 'password'
"""
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']


# clean: ta metoda jest wywoływana automatycznie przez Django podczas walidacji formularza
    def clean(self):
        cleaned_data = super(UserForm, self).clean() # getting data
        print(cleaned_data)
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match" # print in html {{ form.non_filed_errors }}
            )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'pin_code']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
