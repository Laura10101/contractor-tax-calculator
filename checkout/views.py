from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import requests
import json

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    template = 'checkout/checkout.html'

    base_url = request.scheme + '://' + request.get_host()
    url = base_url + '/api/payments/'

    # Get subscription details from form
    if '1_month' in request.POST.keys():
        requested_months = 1
        subtotal = request.POST['1_month']
    elif '3_month' in request.POST.keys():
        requested_months = 3
        subtotal = request.POST['3_month']
    elif '12_month' in request.POST.keys():
        requested_months = 12
        subtotal = request.POST['12_month']

    # Create data payload for POST request to payment API
    data = {
        'subscription_id': None,
        'requested_months': requested_months,
        'subtotal': subtotal,
        'currency': 'GBP',
    }

    # POST data to payment API
    # This will create Stripe payment confirmation and local record 
    print("Creating payment at URL: " + url)
    response = requests.post(url, json=data)
    print('Create payment response: ' + str(response))
    data = json.loads(response.text)
    
    # Extract data from response 
    payment_id = data['payment_id']
    client_secret = data['client_secret']

    context = { 
        'stripe_public_key': stripe_public_key,
        'client_secret_key': client_secret,
        'payment_id': payment_id
    }
    return render(request, template, context)

# Create function for views on checkout status page: talk to payment API to get payment status
def checkout_status(request):
    # Define template
    template = 'checkout/checkout_status.html'
    base_url = request.scheme + '://' + request.get_host() + '/api/payments/'
    # If request method is POST, confirm payment in payments API
    if request.method == 'POST':
        payment_id = request.POST['payment_id']
        url = base_url + str(payment_id) + '/'
        data = {
            'billing_street_1': request.POST['street_address1'],
            'billing_street_2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'stripe_card_id': request.POST['payment_method_id']
        }
        print("Confirming payment at URL: " + url)
        response = requests.patch(url, json=data)
        print('Confirm payment response: ' + str(response))
        data = json.loads(response.text)
        payment_status = 'pending'
    # If request method is GET, get payment status from payments API
    elif request.method == 'GET':
        payment_id = request.GET['payment_id']
        url = base_url + str(payment_id) + '/status/'
        response = requests.get(url)
        data = json.loads(response.text)
        payment_status = data['status']
        failure_reason = data['failure_reason']
    # Build context 
    context = { 
        'payment_id': payment_id,
        'payment_status': payment_status,
        'failure_reason': failure_reason,
        'payment_pending': pamyent_pending,
    }
    # Render template and return 
    return render(request, template, context)