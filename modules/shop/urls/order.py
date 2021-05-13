
from django.urls import path, include
from modules.shop.views.order import order_create

app_name="shop"

urlpatterns = [
    path('create/', order_create, name='order_create'),
]