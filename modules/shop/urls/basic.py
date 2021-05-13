
from django.urls import path, include
from modules.shop.views.basic import index

urlpatterns = [
	path('', index),
]
