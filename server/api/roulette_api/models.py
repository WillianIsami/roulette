from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models import F
from django.db.models.signals import post_save

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}: {self.balance}"
    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.amount} - {self.timestamp}"
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(instance, created, raw, **kwargs):
    if raw or not created:
        return
    Wallet.objects.create(user=instance)


@receiver(post_save, sender=Transaction)
def update_wallet(instance, created, raw, **kwargs):
    if raw or not created:
        return
    wallet = instance.wallet
    wallet.balance = F('balance') + instance.amount
    wallet.save()