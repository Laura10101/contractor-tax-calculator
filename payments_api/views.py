from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from .services import *

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
        subtotal = request.data['total']
        currency = request.data['currency']

        # Invoke service method 
        payment_id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)
        # Create response 
        response = { 'payment_id' : payment_id }
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
        
class StripeWebhooksList(APIView):
    def post(self, request):
        pass