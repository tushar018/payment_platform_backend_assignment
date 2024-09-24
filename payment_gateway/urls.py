from django.contrib import admin
from django.urls import path, include
from payment_gateway.views import CreateCheckoutSessionView, ProductPageView, SuccessView, CancelView, ManualPaymentPageView
from clients.stripe import stripe_webhook

urlpatterns = [
    path('', ProductPageView.as_view(), name='product_page_view'),
    path('admin/', admin.site.urls),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name="session_cancel"),
    path('success/', SuccessView.as_view(), name="session_success"),
    path('create_payment_session/', CreateCheckoutSessionView.as_view(), name='create_payment_session'),
    path('product_page/', ProductPageView.as_view(), name='product_page_view'),
    path('manual_payment/', ManualPaymentPageView.as_view(), name='manual_payment_view'),
]

