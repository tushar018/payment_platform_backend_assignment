from payment_gateway.models import PaymentLink
from datetime import datetime, timedelta
from django.utils import timezone
from payment_gateway.encryption import encrypt_message


def save_payment_link_instance(data):

    encrypted_url = encrypt_message(data.get('payment_url'))

    _ = PaymentLink.objects.create(
        amount=data.get('amount'),
        currency=data.get('currency'),
        description=data.get('description'),
        expiration_date=datetime.fromtimestamp(data.get('expires_at')),
        payment_url=encrypted_url,
        status=data.get('status'),
        session_id=data.get('session_id'),
    )


