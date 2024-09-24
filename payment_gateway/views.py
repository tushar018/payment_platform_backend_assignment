import logging
import traceback
from django.conf import settings

from django.http import JsonResponse
from gateway_platforms.stripe_gateway import StripeGateway
from django.views.generic import TemplateView
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from analytics.mixpanel import mixpanel_client
from payment_gateway.constants import TrackingEvents
from payment_gateway.models import Product
from payment_gateway.serializers.request_response import CreatePaymentSessionRequestSerialiser, CreatePaymentSessionResponseSerialiser

STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLISHABLE_KEY

logger = logging.getLogger(settings.DEBUG_LOGGER_DJANGO)

gateway_to_class_mapping = {
    "stripe": StripeGateway
}


class BaseView(GenericAPIView):
    """
    Base View for API calls with POST method.
    """

    request_serializer = serializers.Serializer
    response_serializer = serializers.Serializer

    def execute_post(self, request, validated_data):
        return {}, status.HTTP_200_OK

    def post(self, request, *args, **kwargs):

        try:
            # validate request
            serializer = self.request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            # get response
            response, status_code = self.execute_post(
                request=request,
                validated_data=validated_data)

            response_serializer = self.response_serializer(data=response)

            print(status_code)
            if status_code == status.HTTP_200_OK:
                response_serializer.is_valid(raise_exception=True)
            else:
                return Response(response, status=status_code)
            if response is None:
                traceback.print_exc()
                raise APIException()

            return Response(response, status=status_code)

        except APIException as e:
            traceback.print_exc()
            raise e
        except Exception as e:
            traceback.print_exc()
            raise APIException(e)


class CreateCheckoutSessionView(BaseView):

    """
    This routes the payment request to the selected gateway.

    Args:
        request, validated_data (after serialization).

    Returns:
        ({}, status): data, response code
    """

    request_serializer = CreatePaymentSessionRequestSerialiser
    response_serializer = CreatePaymentSessionResponseSerialiser
    serializer_class = serializers.Serializer

    def execute_post(self, request, validated_data):
        try:

            mixpanel_client.track_event(event_name=TrackingEvents.PRODUCT_CHECKOUT_CLICKED, properties=validated_data)

            gateway_platform = validated_data.get('gateway_platform')
            data, status_code = gateway_to_class_mapping.get(gateway_platform)().execute_payment(data=validated_data)


            return data, status_code

        except Exception as e:
            logger.exception(f"FAILED TO ROUTE GATEWAY PLATFORM FOR DATA {validated_data}")
            return {'error': str(e)}, status.HTTP_400_BAD_REQUEST


class SuccessView(TemplateView):

    """
    Renders page for payment success.
    """

    mixpanel_client.track_event(event_name=TrackingEvents.STRIPE_PAYMENT_SUCCESS)
    template_name = "success.html"


class CancelView(TemplateView):
    """
    Renders page for payment cancel.
    """

    mixpanel_client.track_event(event_name=TrackingEvents.STRIPE_PAYMENT_FAILED)
    template_name = "cancel.html"


class ProductPageView(TemplateView):
    """
    Renders page for product list and manual payment.
    """

    template_name = "main_page.html"

    def get_context_data(self, **kwargs):
        mixpanel_client.track_event(event_name=TrackingEvents.PRODUCT_PAGE_SEEN)
        products = Product.objects.all()
        context = super(ProductPageView, self).get_context_data(**kwargs)
        context.update({
            "products": products,
            "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY
        })
        return context

    def post(self, request, *args, **kwargs):

        return JsonResponse({"message": "Success! POST request received."})


class ManualPaymentPageView(TemplateView):

    """
    Renders page for manual payment data.
    """

    template_name = "manual_payment.html"

    def get_context_data(self, **kwargs):

        context = super(ManualPaymentPageView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY
        })
        return context
