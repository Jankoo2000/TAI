from django import forms
from .models import User
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