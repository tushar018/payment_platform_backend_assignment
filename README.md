# payment_platform_backend_assignment


Payment platform to integrate multiple gateways

**Setup**

- Clone the repository

- Activate venv

  - python3 -m venv payment_env
  - source payment_env/bin/activate
  - pip install -r requirements.txt


- Run migrations (if any)

  - python manage.py makemigrations
  - python manage.py migrate


- Run the project

  - Terminal 1

    - python manage.py runserver
    - Go to your localhost URL

  - Terminal 2 (Stripe CLI, OPTIONAL FOR WEBHOOK)

    - Setup stripe-cli - https://docs.stripe.com/stripe-cli
    - Modify webhook key in settings - STRIPE_WEBHOOK_KEY
    - stripe listen --forward-to localhost:8000/payment_gateway/webhooks/stripe/
   
- Analytics
  - Mixpanel Link - https://mixpanel.com/s/306EAD
