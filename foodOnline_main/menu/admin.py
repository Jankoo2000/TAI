from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.

# generating slugs automaticly
"""
W Django prepopulated_fieldsatrybut w ModelAdminklasie jest używany do automatycznego 
wypełniania wartości jednego lub więcej pól na podstawie wartości innego pola.
Składnia słownika to {field_to_be_populated: {dependency_field_1, dependency_field_2, ...}}
"""
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name', )}

    list_display = ('vendor', 'category_name', 'slug')


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('food_title', )}

    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available')

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)

