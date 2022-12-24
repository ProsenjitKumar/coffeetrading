from django.contrib import admin
from .models import Networker, Profile, DepositPaymentMethod, DepositConfirmation,\
    WithdrawalRequest


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'number', 'phone', 'updated_at', 'created_at',]
    search_fields = ['number', 'phone']
    list_per_page = 30
    # exclude = ('gender',)


class DepositPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['currency_name', 'updated_at', 'created_at',]
    search_fields = ['currency_name',]
    list_per_page = 30
    exclude = ('slug',)


class DepositConfirmationAdmin(admin.ModelAdmin):
    list_display = ['amount_deposited', 'updated_at', 'created_at',]
    search_fields = ['amount_deposited',]
    list_per_page = 30


class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['amount', 'updated_at', 'created_at',]
    search_fields = ['amount',]
    list_per_page = 30
    exclude = ('slug',)


admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)
admin.site.register(DepositConfirmation, DepositConfirmationAdmin)
admin.site.register(DepositPaymentMethod, DepositPaymentMethodAdmin)
admin.site.register(Networker)
admin.site.register(Profile, ProfileAdmin)
