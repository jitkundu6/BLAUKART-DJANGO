from django.contrib import admin

from .models import Payment, Purchase, Wallet
# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'purpose', 'amount', 'status', 'date_time')

admin.site.register(Purchase)
admin.site.register(Wallet)
