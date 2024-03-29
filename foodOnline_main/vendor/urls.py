from accounts import views as AccountViews
from django.urls import path

from . import views

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name="fooditems_by_category"),
    # <data_type:var_name>

    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>', views.delete_category, name='delete_category'),

    path('menu-builder/food/add', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>', views.delete_food, name='delete_food'),

    path('orders/', AccountViews.vendorOrders, name='vendor_orders'),
    path('order_detail/<str:order_number>/', views.order_detail, name='vendor_order_detail'),

]