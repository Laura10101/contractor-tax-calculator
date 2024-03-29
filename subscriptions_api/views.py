"""Define view methods for subscriptions API."""
from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
import json
from .models import SubscriptionOption
from .services import (
    create_subscription,
    check_subscription,
    update_subscription,
    get_subscription_options,
    get_subscription_option
)


def contains_required_attributes(request, required_attributes):
    """Validate that the request contains expected data."""
    for attribute in required_attributes:
        if attribute not in request.data.keys():
            return False
    return True


class SubscriptionsList(APIView):
    """Create subscriptions list view."""

    def post(self, request):
        """Create a new subscription."""

        # Define the list of required attributes
        required_attributes = [
            'user_id',
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required '
                    + 'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        user_id = request.data['user_id']
        # Invoke service method
        try:
            subscription_id = create_subscription(user_id)
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError:
            return Response(
                {
                    'error': 'Multiple subscriptions found for user. Please ' +
                    'ask your administrator to resolve this.'
                },
                status=status.HTTP_409_CONFLICT
            )

        # Create response
        response = {
            'subscription_id': subscription_id
        }
        # Return response
        return Response(response)

    def patch(self, request):
        """Extend a user's subscription."""

        # Define the list of required attributes
        required_attributes = [
            'user_id',
            'subscription_option_id',
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        user_id = request.data['user_id']
        subscription_option_id = request.data['subscription_option_id']
        # Invoke service method
        try:
            update_subscription(user_id, subscription_option_id)
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except SubscriptionOption.DoesNotExist:
            return Response(
                {
                    'error': 'Please supply a valid subcription option id'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError:
            return Response(
                {
                    'error': 'Multiple subscriptions found for user. Please ' +
                    'ask your administrator to resolve this.'
                },
                status=status.HTTP_409_CONFLICT
            )
        # Generate and return response
        response = {}
        # Return response
        return Response(response)


class SubscriptionOptionsList(APIView):
    """Create subscription options list view."""

    def get(self, request):
        """Get a list of available subscription options."""

        all_options = get_subscription_options()

        serialised_options = []
        for option in all_options:
            serialised_options.append({
                'id': option.id,
                'subscription_months': option.subscription_months,
                'subscription_price': option.subscription_price,
                'vat': option.vat(),
                'total_price': option.total(),
            })

        response = {
            'subscription_options': serialised_options
        }
        return Response(response)


class SubscriptionOptionDetail(APIView):
    """Create subscription option detail view."""

    def get(self, request, pk):
        """Retrieve a specific subscription option by ID."""

        option = get_subscription_option(pk)
        serialized_option = {
            'id': option.id,
            'subscription_months': option.subscription_months,
            'subscription_price': option.subscription_price,
            'vat': option.vat(),
            'total': option.total(),
        }
        response = {
            'subscription_option': serialized_option
        }
        return Response(response)


class SubscriptionStatusesList(APIView):
    """Create subscription statuses list view."""

    def get(self, request):
        """Get the subscription status for a given user."""

        # Extract user_id
        if 'user_id' not in request.GET.keys():
            # Code to return an HTTP 400 error
            # https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django
            return Response(
                {
                    'error': 'Invalid request. Please specify user ID for ' +
                    'which to check the status'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user_id = int(request.GET['user_id'])
        try:
            is_active = check_subscription(user_id)
        except Exception:
            return Response(
                {
                    'error': 'Something went wrong when retrieving ' +
                    'subscription status for this user. Please ' +
                    'contact your admin'
                },
                status=status.HTTP_409_CONFLICT
            )
        # Package the JSON data up into a response object
        response = {
            'user_id': user_id,
            'has_active_subscription': is_active
        }
        # Sending the Json response back to the client
        return Response(response)
