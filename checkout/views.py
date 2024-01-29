from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import requests
import json

# Create your views here.
@login_required
def checkout(request):
    template = 'checkout/checkout.html'

    if request.method != 'POST':
        return redirect(reverse('subscription'))

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    base_url = request.scheme + '://' + request.get_host()
    
    # Get subscription option id from form
    subscription_option_id = int(request.POST.get('subscription'))

    # Get the subscription option from the subscription API
    url = base_url + '/api/subscriptions/options/'
    response = requests.get(url + str(subscription_option_id))

    if response.status_code == 404:
        return render(request, template, { 'error': 'Failed to find subscription option with id ' + str(subscription_option_id) })

    try:
        option_data = json.loads(response.text)['subscription_option']
    except:
        return render(request, template, { 'error': 'Failed to retrieve subscription option with response code ' + str(response.status_code) })

    if 'error' in option_data:
        return render(request, template, { 'error': 'Failed to retrieve subscription option with error ' + option_data['error'] })
    
    # Create data payload for POST request to payment API
    data = {
        'user_id': request.user.id,
        'subscription_option_id': subscription_option_id,
        'total': option_data['total'],
        'currency': 'GBP',
    }

    # POST data to payment API
    # This will create Stripe payment confirmation and local record 
    response = requests.post(url, json=data)

    try:
        option_data = json.loads(response.text)['subscription_option']
    except:
        return render(request, template, { 'error': 'Failed to retrieve subscription option with response code ' + str(response.status_code) })

    if 'error' in option_data:
        return render(request, template, { 'error': 'Failed to retrieve subscription option with error ' + option_data['error'] })

    payment_result = json.loads(response.text)
    payment_id, client_secret = payment_result['payment_id'], payment_result['client_secret']

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

@login_required
def confirm_checkout(request):
    # Define template
    template = 'checkout/checkout_status.html'
    base_url = request.scheme + '://' + request.get_host()

    if not request.method == 'POST':
        return redirect(reverse('subscription'))

    payment_id = request.POST['payment_id']
    print('Confirming payment with local id of ' + str(payment_id))
    url = base_url + '/api/payments/' + str(payment_id) + '/'
    data = {
        'stripe_card_id': request.POST['payment_method_id']
    }
    if 'street_address2' in request.POST:
        data['billing_street_2'] = request.POST['street_address2'],
    print("Confirming payment at URL: " + url)
    response = requests.patch(url, json=data)
    
    if response.status_code == 404:
        return render(request, template, { 'error': 'Failed to find payment with id ' + str(payment_id) })

    try:
        data = json.loads(response.text)
    except:
        return render(request, template, { 'error': 'Failed to confirm payment with response code ' + str(response.status_code) })

    if 'error' in data:
        return render(request, template, { 'error': 'Failed to confirm payment with error: ' + data['error'] })

    if data['result'] in ['processing', 'succeeded']:
        # Display success to user
        return redirect('/contractors/checkout/status/' + str(payment_id) + '/')
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
@login_required
def checkout_status(request, id):
    # Define template
    template = 'checkout/checkout_status.html'
    base_url = request.scheme + '://' + request.get_host() + '/api/payments/'
    failure_reason = ''

    if not request.method == 'GET':
        return redirect(reverse('contractor_home'))
    
    # Get payment status from payments API
    url = base_url + str(id) + '/status/'
    print('Checking payment status at url = ' + url)
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 404:
        return render(request, template, {
             'error': 'No payment could be found for id ' + str(id) + 
             '. Please search find your payment on <a href="' + reverse('contractor_home') + '">your dashboard</a>.' })
    try:
        data = json.loads(response.text)
    except:
        return render(request, template, { "error": 'Failed to load payment with ' + str(id) + '. Received response code ' + str(response.status_code) })
    
    if 'error' in data:
        return render(request, template, { "error": data['error'] })

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