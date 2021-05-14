#from django.conf.urls import include, url

from modules.shop.urls import basic
from modules.shop.urls import cart
from modules.shop.urls import order

from django.urls import path, include, re_path

app_name ='shop'

urlpatterns = [
    re_path('', include(basic,  namespace='basic')),
    re_path(r'^cart/', include(cart, namespace='cart')),
    re_path(r'^order/', include(order,  namespace='orders')),
]
