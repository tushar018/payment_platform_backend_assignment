from django.utils import timezone
from rest_framework import serializers
from payment_gateway.models import PaymentLink


class CreatePaymentSessionRequestSerialiser(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField(required=True)
    description = serializers.CharField(max_length=512)
    name = serializers.CharField(max_length=128)
    expiration_hours = serializers.IntegerField()
    gateway_platform = serializers.CharField(max_length=128)


class CreatePaymentSessionResponseSerialiser(serializers.Serializer):
    id = serializers.CharField(allow_null=True)


class PaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLink
        fields = '__all__'
