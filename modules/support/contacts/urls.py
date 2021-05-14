
from django.urls import path, include

from . import views


app_name = 'contacts'

urlpatterns = [
    path('contact/', views.form_submit, name="contact"),
]


