from django.urls import path

from . import views

#from apps.payments.views import payment,payment_success

urlpatterns = [
    path('payments/<int:id>/', views.payment_initiate, name="payments"),
    path('payments/success/', views.payment_success, name="payment-success"),
]