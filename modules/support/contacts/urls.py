
from django.urls import path, include

from . import views

urlpatterns = [
    path('contact/', views.form_submit, name="contact"),
]


