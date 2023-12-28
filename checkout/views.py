from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import requests
import json

# Helper functions
# Get details of a subscription option based on its id
def get_subscription_option(base_url, subscription_option_id):
    url = base_url + '/api/subscriptions/options/'
    response = requests.get(url + str(subscription_option_id))
    print('Subscription option response: ' + response.text)
    return json.loads(response.text)['subscription_option']

def post_payment(base_url, user_id, subscription_option_id, total, currency):
    url = base_url + '/api/payments/'

    # Create data payload for POST request to payment API
    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency,
    }

    # POST data to payment API
    # This will create Stripe payment confirmation and local record 
    response = requests.post(url, json=data)
    if not response.ok:
        raise Exception('An unexpected error occurred when posting payment with HTTP status of: ' + str(response.status_code))
    payment_result = json.loads(response.text)
    return payment_result['payment_id'], payment_result['client_secret']

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    template = 'checkout/checkout.html'
    base_url = request.scheme + '://' + request.get_host()
    
    # Get subscription option id from form
    subscription_option_id = int(request.POST.get('subscription'))

    # Get the subscription option from the subscription API
    option_data = get_subscription_option(base_url, subscription_option_id)

    # Extract data from response 
    payment_id, client_secret = post_payment(
        base_url,
        request.user.id,
        subscription_option_id,
        option_data['total'],
        'GBP',
    )

    context = { 
        'stripe_public_key': stripe_public_key,
        'client_secret_key': client_secret,
        'payment_id': payment_id,
        'subscription_option_id': subscription_option_id,
        'subscription_months': option_data['subscription_months'],
        'subscription_price': option_data['subscription_price'],
        'vat': option_data['vat'],
        'total': option_data['total'],
    }
    return render(request, template, context)

def confirm_checkout(request):
    # Define template
    template = 'checkout/checkout_status.html'
    base_url = request.scheme + '://' + request.get_host()

    if not request.method == 'POST':
        raise SuspiciousOperation('Invalid request. This view may only be accessed via the checkout form.')

    payment_id = request.POST['payment_id']
    print('Confirming payment with local id of ' + str(payment_id))
    url = base_url + '/api/payments/' + str(payment_id) + '/'
    data = {
        'billing_street_1': request.POST['street_address1'],
        'town_or_city': request.POST['town_or_city'],
        'county': request.POST['county'],
        'country': request.POST['country'],
        'postcode': request.POST['postcode'],
        'stripe_card_id': request.POST['payment_method_id']
    }
    if 'street_address2' in request.POST:
        data['billing_street_2'] = request.POST['street_address2'],
    print("Confirming payment at URL: " + url)
    response = requests.patch(url, json=data)
    if not response:
        raise Exception('Failed to confirm payment')
    print('Confirm payment response: ' + str(response))
    data = json.loads(response.text)
    if data['result'] in ['processing', 'succeeded']:
        # Display success to user
        return redirect('/checkout/status/' + str(payment_id) + '/')
    else:
        payment_status = 'failed'
        failure_reason = data['result']
    context = { 
        'payment_id': payment_id,
        'payment_status': payment_status,
        'failure_reason': failure_reason,
        'payment_pending': payment_status == 'pending',
    }
    return render(request, template, context)

# Create function for views on checkout status page: talk to payment API to get payment status
def checkout_status(request, id):
    # Define template
    template = 'checkout/checkout_status.html'
    base_url = request.scheme + '://' + request.get_host() + '/api/payments/'
    failure_reason = ''

    if not request.method == 'GET':
        raise SuspiciousOperation('Invalid request. This view must be accessed via a GET request.')
    
    # Get payment status from payments API
    url = base_url + str(id) + '/status/'
    print('Checking payment status at url = ' + url)
    response = requests.get(url)
    data = json.loads(response.text)
    payment_status = data['status']
    failure_reason = data['failure_reason']
    # Build context 
    context = { 
        'payment_id': id,
        'payment_status': payment_status,
        'failure_reason': failure_reason,
        'payment_pending': payment_status == 'pending',
    }
    # Render template and return 
    return render(request, template, context)