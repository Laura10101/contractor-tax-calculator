from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from stripe.error import InvalidRequestError
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
            'subscription_option_id',
            'total',
            'currency',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=400
                )
        
        # Extract data required for service method
        subscription_id = request.data['subscription_id']
        subscription_option_id = request.data['subscription_option_id']
        total = request.data['total']
        currency = request.data['currency']

        if not isinstance(subscription_id, int) or subscription_id < 0:
            return Response({ 'error': 'Subscription with id = ' + str(subscription_id) + ' could not be found.' }, status=404)
        
        if not isinstance(subscription_option_id, int) or subscription_option_id < 0:
            return Response({ 'error': 'Subscription option with id = ' + str(subscription_option_id) + ' could not be found.' }, status=404)

        # Invoke service method 
        try:
            payment_id, client_secret = create_payment(subscription_id, subscription_option_id, total, currency)
        except ValidationError as e:
            return Response(
                { 'error' : str(e) },
                status=400
                )
        except InvalidRequestError as e:
            return Response(
                { 'error' : str(e) },
                status=400
                )
        # Create response 
        response = {
            'payment_id' : payment_id,
            'client_secret': client_secret,
        }
        # Return response 
        return Response(response)

class PaymentDetail(APIView):
    def patch(self, request, pk):
        required_attributes = [
            'stripe_card_id',
        ]

        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=400
                )
        
        # Extract data required for service method
        stripe_card_id = request.data['stripe_card_id']

        # Invoke service method 
        try:
            succeeded, result = confirm_payment(pk, stripe_card_id)
        except Payment.DoesNotExist:
            return Response(status=404)
        except stripe.error.InvalidRequestError as e:
            return Response(
                { 'error' : str(e) },
                status=400
                )
        # Create response 
        response = {
            'succeeded': succeeded,
            'result': result,
            }
        # Return response 
        return Response(response)

class PaymentStatusDetail(APIView):
    def get(self, request, pk):
        status, failure_reason = get_payment_status(id)
        response = {
            'id': id,
            'status': status,
            'failure_reason': failure_reason,
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
                json.dumps(request.data), sig_header, wh_secret
            )
        except Exception as e:
            print(str(e))
            return Response(
                { 'error' : str(e) },
                status=400
                )

        # Does it contain all of the attributes expected?
        if 'type' not in request.data.keys():
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=400
                )

        if 'id' not in request.data['data']['object'].keys():
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=400
                )

        if 'status' not in request.data['data']['object'].keys():
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=400
                )

        # Extract the attributes from the webhook request
        event_type = request.data['type']
        stripe_pid = request.data['data']['object']['id']
        status = request.data['data']['object']['status']
        # Call the apropriate services function based on the event type
        # Create switch statmeent to determine which event type has occurred 
        try:
            match event_type:
                case 'payment_intent.canceled':
                    fail_payment(stripe_pid, status)
                case 'payment_intent.payment_failed':
                    fail_payment(stripe_pid, status)
                case 'payment_intent.requires_action':
                    fail_payment(stripe_pid, status)
                case 'payment_intent.succeeded':
                    complete_payment(stripe_pid)
        except Payment.DoesNotExist:
            return Response(status=404)
        # Return response 
        return Response({}, status=200)