from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    CURRENCY_CHOICES = [
        ('ETH', 'Ethereum'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Currency")
    public_key = models.CharField(max_length=200, verbose_name="Public Key")
    private_key = models.CharField(max_length=200, verbose_name="Private Key")
    balance = models.FloatField(default=0, verbose_name="Wallet Balance")

    def __str__(self):
        return f'{self.currency} Wallet {self.id}'
