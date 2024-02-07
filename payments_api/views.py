"""Define view methods for the payment API."""

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from stripe.error import InvalidRequestError
from .services import (
    create_payment,
    confirm_payment,
    complete_payment,
    fail_payment,
    get_payment_status,
    get_recent_payments
)
import json
import stripe


def contains_required_attributes(request, required_attributes):
    """Validate that the given request contains expected data."""

    for attribute in required_attributes:
        if attribute not in request.data.keys():
            return False
    return True


class PaymentsList(APIView):
    """Create Payments List view."""

    def get(self, request):
        """Get a list of recent payments for the given user id."""

        # Validate data
        if 'user_id' not in request.GET:
            return Response(
                {
                    'error': 'Invalid request. Please supply all required '
                    + 'attributes.'
                },
                status=400
            )

        # Extract data required for service method
        user_id = request.GET['user_id']

        try:
            payments = get_recent_payments(user_id)
        except Exception as e:
            return Response(
                {
                    'error': str(e)
                },
                status=404
            )

        # Create response
        payment_statuses = {
            -1: 'failed',
            1: 'created',
            2: 'intended',
            3: 'pending',
            4: 'complete',
        }
        response = []
        for payment in payments.all():
            response.append({
                'id': payment.id,
                'created_date': payment.created_date,
                'completed_date': payment.completed_or_failed_date,
                'total': payment.total,
                'status': payment_statuses[payment.status]
            })

        # Return response
        return Response(response)

    def post(self, request):
        """Create a new payment and payment intention."""

        required_attributes = [
            'user_id',
            'subscription_option_id',
            'total',
            'currency',
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=400
            )

        # Extract data required for service method
        user_id = request.data['user_id']
        subscription_option_id = request.data['subscription_option_id']
        total = request.data['total']
        currency = request.data['currency']

        if not isinstance(user_id, int) or user_id < 0:
            return Response(
                {
                    'error': 'User with id ' + str(user_id) +
                    ' could not be found.'
                },
                status=404
            )

        if not isinstance(subscription_option_id, int)
        or subscription_option_id < 0:
            return Response(
                {
                    'error': 'Subscription option with id ' +
                    str(subscription_option_id) + ' could not be found.'
                },
                status=404
            )

        # Invoke service method
        try:
            payment_id, client_secret = create_payment(
                user_id,
                subscription_option_id,
                total,
                currency
            )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=400
            )
        except InvalidRequestError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=400
            )
        # Create response
        response = {
            'payment_id': payment_id,
            'client_secret': client_secret,
        }
        # Return response
        return Response(response)


class PaymentDetail(APIView):
    """Create Payment detail API view."""

    def patch(self, request, pk):
        """Update a payment with the Stripe card ID."""
        """This will confirm the payment with Stripe."""

        required_attributes = [
            'stripe_card_id',
        ]

        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=400
            )

        # Extract data required for service method
        stripe_card_id = request.data['stripe_card_id']

        # Invoke service method
        try:
            result = confirm_payment(pk, stripe_card_id)
        except Payment.DoesNotExist:
            return Response(status=404)
        except stripe.error.InvalidRequestError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=400
            )
        # Create response
        response = {
            'result': result,
        }
        # Return response
        return Response(response)


class PaymentStatusDetail(APIView):
    """Create API view to retrieve payment status."""

    def get(self, request, pk):
        """Return the current status of the given payment."""

        try:
            status, failure_reason = get_payment_status(pk)
        except Payment.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response(
                {
                    'error': str(e)
                },
                status=400
            )

        response = {
            'id': pk,
            'status': status,
            'failure_reason': failure_reason,
        }
        return Response(response)


class StripeWebhooksList(APIView):
    """Create API view to receive Stripe webhooks."""

    def post(self, request):
        """Receive webhooks from Stripe."""
        """Update the payment status to either completed"""
        """or failed in response."""

        # Validate the webhook signature for security purposes
        # This is taken from the Boutique ADO video by Tim Nelson
        wh_secret = settings.STRIPE_WH_SECRET
        stripe.api_key = settings.STRIPE_SECRET_KEY
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                request.body.decode('utf-8'), sig_header, wh_secret
            )
        except Exception as e:
            return Response(
                {
                    'error': str(e)
                },
                status=400
            )

        # Does it contain all of the attributes expected?
        if 'type' not in request.data.keys():
            return Response(
                {
                    'error': 'Invalid request. Please supply all ' +
                    'required attributes.'
                },
                status=400
            )

        if 'id' not in request.data['data']['object'].keys():
            return Response(
                {
                    'error': 'Invalid request. Please supply ' +
                    'all required attributes.'
                },
                status=400
            )

        if 'status' not in request.data['data']['object'].keys():
            return Response(
                {
                    'error': 'Invalid request. Please supply all ' +
                    'required attributes.'
                },
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
            return Response(
                {
                    'error': 'Payment with stripe_pid ' +
                    str(stripe_pid) + ' not found.'
                },
                status=404
            )
        # Return response
        return Response({}, status=200)
