from django.contrib import admin

# Register your models here.
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email')
    search_fields=('name','email')
admin.site.register(Contact,ContactAdmin)
