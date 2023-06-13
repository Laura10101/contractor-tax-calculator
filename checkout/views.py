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
    response = requests.post(url, json=data)
    print(response)
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