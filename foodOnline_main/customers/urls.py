from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.custDashboard, name='customers'),
    path('profile/', views.cprofile, name='cprofile'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_details/<str:order_number>', views.order_details, name='order_details'),
]