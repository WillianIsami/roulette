from django.contrib import admin
from roulette_api.models import Wallet, Transaction

# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'balance'
    ]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'wallet',
        'amount',
        'timestamp'
    ]
