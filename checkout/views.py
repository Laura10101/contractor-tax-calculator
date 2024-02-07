"""Define views for the checkout app."""

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import requests
import json


@login_required
def checkout(request):
    """Create the payment intent and display the checkout form."""
    template = 'checkout/checkout.html'

    # Prevent access to the checkout view via non-post methods
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

    # Return an error if the response was not found
    if response.status_code == 404:
        return render(
            request,
            template,
            {
                'error': 'Failed to find subscription option with id '
                + str(subscription_option_id)
            }
        )

    # Try to parse the subscription option data
    # If this fails, return an exception
    try:
        data = json.loads(response.text)
        option_data = data['subscription_option']
    except Exception:
        return render(
            request,
            template,
            {
                'error': 'Failed to fetch subscription option with status ' +
                str(response.status_code)
            }
        )

    # If the response contains an error, display
    # a more friendly error
    if 'error' in option_data:
        return render(
            request,
            template,
            {
                'error': 'Failed to retrieve subscription option with error ' +
                option_data['error']
            }
        )

    # Create data payload for POST request to payment API
    data = {
        'user_id': request.user.id,
        'subscription_option_id': subscription_option_id,
        'total': option_data['total'],
        'currency': 'GBP',
    }

    # POST data to payment API
    # This will create Stripe payment confirmation and local record
    url = base_url + '/api/payments/'
    response = requests.post(url, json=data)
    print(response.text)

    # Parse the payment result and return an error if the result
    # could not be parsed correctly
    try:
        payment_result = json.loads(response.text)
        payment_id = payment_result['payment_id']
        client_secret = payment_result['client_secret']
    except Exception:
        return render(
            request,
            template,
            {
                'error': 'Failed to create payment intent with status ' +
                str(response.status_code)
            }
        )

    # If an error is contained in the response,
    # display it to the user
    if 'error' in option_data:
        return render(
            request,
            template,
            {
                'error': 'Failed to create payment intent with error: ' +
                option_data['error']
            }
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


@login_required
def confirm_checkout(request):
    """Handle the submitted checkout form."""
    """Confirm the payment via the payment API"""
    """If successful, redirect to the status page"""
    """Otherwise, display an error."""
    # Define template
    template = 'checkout/checkout_status.html'
    base_url = request.scheme + '://' + request.get_host()

    # Prevent the user from accessing the view except via
    # a POST request
    if not request.method == 'POST':
        return redirect(reverse('subscription'))

    # Confirm the payment via the payment API
    payment_id = request.POST['payment_id']
    url = base_url + '/api/payments/' + str(payment_id) + '/'
    data = {
        'stripe_card_id': request.POST['payment_method_id']
    }
    if 'street_address2' in request.POST:
        data['billing_street_2'] = request.POST['street_address2'],
    response = requests.patch(url, json=data)

    # If the result of payment confirmation is not found,
    # display an error
    if response.status_code == 404:
        return render(
            request,
            template,
            {
                'error': 'Failed to find payment with id ' +
                str(payment_id)
            }
        )

    # Try and parse the payment confirmation response
    # And if this fails, display an error
    try:
        data = json.loads(response.text)
    except Exception:
        return render(
            request,
            template,
            {
                'error': 'Failed to confirm payment with response code ' +
                str(response.status_code)
            }
        )

    # If an error is found in the response,
    # display it to the user
    if 'error' in data:
        return render(
            request,
            template,
            {
                'error': 'Failed to confirm payment with error: ' +
                data['error']
            }
        )

    # If the payment succeeded, redirect to the status page
    if data['result'] in ['processing', 'succeeded']:
        # Display success to user
        endpoint = '/contractors/checkout/status/' + str(payment_id) + '/'
        return redirect(endpoint)
    else:
        # Otherwise, display a failure message
        payment_status = 'failed'
        failure_reason = data['result']
    context = {
        'payment_id': payment_id,
        'payment_status': payment_status,
        'failure_reason': failure_reason,
        'payment_pending': payment_status == 'pending',
    }
    return render(request, template, context)


@login_required
def checkout_status(request, id):
    """Display the status of a given payment to the user."""
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

    # Return an error if the response is not found
    if response.status_code == 404:
        return render(
            request,
            template,
            {
                'error': 'No payment could be found for id ' + str(id) +
                '. Please search find your payment on <a href="' +
                reverse('contractor_home') + '">your dashboard</a>.'
            }
        )

    # Try and parse the payment status
    # If it fails, display an error
    try:
        data = json.loads(response.text)
    except Exception:
        return render(
            request,
            template,
            {
                "error": 'Failed to load payment with ' +
                str(id) +
                '. Received response code ' + str(response.status_code)
            }
        )

    # If an error is found in the response,
    # display it to the user
    if 'error' in data:
        return render(
            request,
            template,
            {
                "error": data['error']
            }
        )

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
