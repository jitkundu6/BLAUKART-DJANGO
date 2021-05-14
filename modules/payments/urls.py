from django.urls import path

from . import views

#from apps.payments.views import payment,payment_success

app_name = 'payments'

urlpatterns = [
    path('<int:id>/', views.payment_initiate, name="payments"),
    path('success/', views.payment_success, name="payment-success"),
]