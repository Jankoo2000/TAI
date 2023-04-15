from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email','username', 'first_name', 'last_name', 'role', 'is_active') # displaying in admin panel
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



# displaying User in admin panel
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
