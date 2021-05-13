from django.urls import path, include
from modules.shop.views.cart import cart_detail, cart_add, cart_remove

app_name="shop"

urlpatterns = [
	path('', cart_detail, name='cart_detail'),
	path('add/<int:product_id>/',
	     cart_add,
	     name='cart_add'),
	path('remove/<int:product_id>/',
	     cart_remove,
	     name='cart_remove'),
]
