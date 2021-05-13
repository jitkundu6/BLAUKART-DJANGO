#from django.conf.urls import include, url
from modules.shop.urls import basic

from django.urls import path, include

app_name = 'modules.shop'

urlpatterns = [
    path('', include(basic)),
]
