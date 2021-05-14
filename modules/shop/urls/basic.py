from django.urls import path, include
from modules.shop.views.basic import index, product_list, product_detail

app_name="shop"

urlpatterns = [
	path('', index,  name='index'),
	path('', index,  name='home'),
	
	path('products/', product_list, name='product_list'),
	path('products/<slug:category_slug>/', product_list,
	     name='product_list_by_category'),
	path('products/<int:id>/<slug:slug>/', product_detail,
	     name='product_detail'),
]
