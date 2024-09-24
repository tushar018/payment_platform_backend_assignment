from django.db import models

# Create your models here.
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=128)
    expiry_time = models.IntegerField(default=24)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    def get_price(self):
        return "{0:.2f}".format(self.price / 100)


class PaymentLink(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    description = models.TextField(null=True)
    expiration_date = models.DateTimeField(null=True)
    payment_url = models.URLField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=512)

    def __str__(self):
        return f"PaymentLink {self.id} - {self.status}"
