from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import *
import json
import stripe

# Create a function to validate that a request contains
# the required attributes, so the API views can use it
def contains_required_attributes(request, required_attributes):
    for attribute in required_attributes:
            if attribute not in request.data.keys():
                return False
    return True

# Create your views here.
class PaymentsList(APIView):
    def post(self, request):
        required_attributes = [
            'subscription_id',
            'requested_months',
            'subtotal',
            'currency',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method
        subscription_id = request.data['subscription_id']
        requested_subscription_months = request.data['requested_months']
        try:
            subtotal = int(request.data['subtotal'])
        except ValueError:
            return Response(
                { 'error' : 'Subtotal must be a numeric value.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        currency = request.data['currency']

        # Invoke service method 
        payment_id, client_secret = create_payment(subscription_id, requested_subscription_months, subtotal, currency)
        # Create response 
        response = {
            'payment_id' : payment_id,
            'client_secret': client_secret,
        }
        # Return response 
        return Response(response)

class PaymentDetail(APIView):
    def patch(self, request, id):
        required_attributes = [
            'billing_street_1',
            'billing_street_2',
            'town_or_city',
            'county',
            'country',
            'postcode',
            'stripe_card_id'
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # Extract data required for service method
        billing_street_1 = request.data['billing_street_1']
        billing_street_2 = request.data['billing_street_2']
        town_or_city = request.data['town_or_city']
        county = request.data['county']
        country = request.data['country']
        postcode = request.data['postcode']
        stripe_card_id = request.data['stripe_card_id']

        # Invoke service method 
        confirm_payment(id, billing_street_1, billing_street_2, town_or_city, county, country, postcode, stripe_card_id)
        # Create response 
        response = { }
        # Return response 
        return Response(response)

class PaymentStatusDetail(APIView):
    def get(self, request, id):
        status = get_payment_status(id)
        response = {
            'id': id,
            'status': status
        }
        return Response(response)
        
class StripeWebhooksList(APIView):
    # Create function to handle webhooks from Stripe
    def post(self, request):
        # Validate the webhook signature for security purposes
        # This is taken from the Boutique ADO video by Tim Nelson
        wh_secret = settings.STRIPE_WH_SECRET
        stripe.api_key = settings.STRIPE_SECRET_KEY
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                request.data, sig_header, wh_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(content=e, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(content=e, status=400)
        except Exception as e:
            return HttpResponse(content=e, status=400)

        # Does it contain all of the attributes expected?
        if 'type' not in request.data.keys():
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )

        if 'id' not in request.data['data']['object'].keys():
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )

        if 'status' not in request.data['data']['object'].keys():
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )

        # Extract the attributes from the webhook request
        event_type = request.data['type']
        stripe_pid = request.data['data']['object']['id']
        status = request.data['data']['object']['status']
        # Call the apropriate services function based on the event type
        # Create switch statmeent to determine which event type has occurred 
        match event_type:
            case 'payment_intent.canceled':
                fail_payment(stripe_pid, status)
            case 'payment_intent.payment_failed':
                fail_payment(stripe_pid, status)
            case 'payment_intent.requires_action':
                fail_payment(stripe_pid, status)
            case 'payment_intent.succeeded':
                complete_payment(stripe_pid)
        # Return response 
        return HttpResponse((f'Webhook successfully processed: {event["type"]}'), status=200)