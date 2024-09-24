import logging
from django.conf import settings
from rest_framework import status
from clients.stripe import StripeServiceClient
from payment_gateway.utils import save_payment_link_instance

logger = logging.getLogger(settings.DEBUG_LOGGER_DJANGO)


class StripeGateway:

    """
    Initiates the flow for stripe gateway payment
    and routes the request to gateway client.

    Args:
        data -> request data

    Returns:
        ({}, status): data, response code
    """

    def execute_payment(self, data):
        try:

            session = StripeServiceClient.create_session(data=data)
            print(session)

            payment_data = {
                "amount": session.amount_total,
                "currency": session.currency,
                "description": None,
                "expiration_date": session.expires_at,
                "payment_url": session.url,
                "status": session.status,
                "session_id": session.id,
                "expires_at": session.expires_at
            }

            save_payment_link_instance(data=payment_data)

            return {'id': session.id}, status.HTTP_200_OK

        except:
            logger.exception(f"FAILED TO EXECUTE PAYMENT FOR STRIPE FOR DATA {data}")


