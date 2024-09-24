from django.apps import AppConfig
from django.contrib import admin


class PaymentGatewayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment_gateway'
