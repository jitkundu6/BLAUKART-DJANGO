from django.contrib import admin
from . models import CustomUser, AuthToken

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(AuthToken)