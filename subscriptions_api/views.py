from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
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
class SubscriptionsList(APIView):
    def post(self, request):
        # Define the list of required attributes 
        required_attributes = [
            'user_id',
            'subscription_months',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        user_id = request.data['user_id']
        susbcription_months = request.data['subscription_months']
        # Invoke service method 
        subscription_id = create_subscription(user_id, subscription_months)
        # Create response 
        response = { 'subscription_id' : subscription_id }
        # Return response 
        return Response(response)

class SubscriptionDetail(APIView):
    def patch(self, request, pk):
        # Define the list of required attributes 
        required_attributes = [
            'subscription_months',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        susbcription_months = request.data['subscription_months']
        # Invoke service method
        update_subscription(pk, subscription_months)
        # Generate and return response 
        response = { }
        # Return response 
        return Response(response)

class SubscriptionStatusesList(APIView):
    def get(self, request):
        # Extract user_id
        if 'user_id' not in request.GET.keys():
            # Code to return an HTTP 400 error
            # From: https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django
            return Response(
                { 'error' : 'Invalid request. Please specify user ID for which to check the status' },
                status=status.HTTP_400_BAD_REQUEST
                )
        user_id = int(request.GET['user_id'])
        try:
            is_active = check_subscription(user_id)
        except:
            return Response(
                { 'error' : 'Something went wrong when retrieving subscription status for this user.\
                 Please contact your admin' },
                status=status.HTTP_409_CONFLICT
                )
        # Package the JSON data up into a response object
        response = { 
            'user_id': user_id,
            'has_active_subscription' : is_active
             }
        # Sending the Json response back to the client
        return Response(response)