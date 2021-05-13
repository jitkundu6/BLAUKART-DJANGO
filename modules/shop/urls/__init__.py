#from django.conf.urls import include, url

from modules.shop.urls import basic
from modules.shop.urls import cart
from modules.shop.urls import order

from django.urls import path, include


urlpatterns = [
    path('', include(basic,  namespace='shop')),
    path('cart/', include(cart, namespace='cart')),
    path('order/', include(order,  namespace='orders')),
]
