import logging
import stripe
from django.conf import settings
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from payment_gateway.models import PaymentLink
from django.http import HttpResponse
from analytics.mixpanel import mixpanel_client
from payment_gateway.constants import TrackingEvents

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(settings.DEBUG_LOGGER_DJANGO)


class StripeServiceClient:

    """
    Makes the third-party API call to stripe.
    """

    @classmethod
    def create_session(cls, data):
        try:
            currency = data.get('currency', 'usd')
            amount = data.get('amount')
            expiration_hours = data.get('expiration_hours')
            name = data.get('name')

            mixpanel_client.track_event(event_name=TrackingEvents.STRIPE_API_CALLED_FOR_PAYMENT_LINK, properties=data)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': name,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                metadata={
                    "product_name": name
                },
                mode='payment',
                success_url='http://127.0.0.1:8000/payment_gateway/success/',
                cancel_url='http://127.0.0.1:8000/payment_gateway/cancel/',
                expires_at=datetime.now() + timedelta(hours=expiration_hours)
            )

            mixpanel_client.track_event(event_name=TrackingEvents.STRIPE_API_CALLED_FOR_PAYMENT_LINK_RESPONSE,
                                        properties={
                                            "status": session.get('status'),
                                            "amount": session.get('amount_total'),
                                            "currency": session.get('currency'),
                                            "created": datetime.fromtimestamp(session.get('created')),
                                            "expires_at": datetime.fromtimestamp(session.get('expires_at')),
                                            "payment_method_types": session.get('payment_method_types')
                                        })

        except:
            logger.exception(f"FAILED TO HIT STRIPE SERVICE FOR PRODUCT {data.get('name')}")
            session = {}

        return session


@csrf_exempt
def stripe_webhook(request):

    """
    Webhook to receive and store payment feedback from stripe.
    """

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    print("ID IS", event['data']['object']['id'])

    if (
    event['type'] == 'checkout.session.completed'
    or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        session = event['data']['object']
        try:
            mixpanel_client.track_event(
                event_name=TrackingEvents.STRIPE_WEBHOOK_FEEDBACK_RECEIVED,
                properties={'status': "success", "amount": session.amount_total}
            )
            payment_link = PaymentLink.objects.get(session_id=session.id)
            payment_link.status = 'success'
            payment_link.save()

        except PaymentLink.DoesNotExist:
            print("PAYMENT LINK DOESN'T EXIST")

    return HttpResponse(status=200)
