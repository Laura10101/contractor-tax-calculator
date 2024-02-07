"""Define views for the home app."""

from django.shortcuts import render
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from .helpers import *


def index(request):
    """Display the main index page for the site."""

    template = 'home/index.html'
    context = {
    }

    return render(request, template, context)


def contractor_index(request):
    """Display the index page for contractors."""

    template = 'home/contractor_index.html'
    context = {
    }

    return render(request, template, context)


@admin.site.admin_view
def admin_index(request):
    """Display the index page for admin users."""

    template = 'home/admin_index.html'
    context = {
    }

    return render(request, template, context)


@login_required
def home(request):
    """Display the contractor home page and dashboard."""

    template = 'home/home.html'
    base_url = request.scheme + '://' + request.get_host()

    user_id = request.user.id
    username = request.user.username

    context = {}

    # Add subscription status to the context
    try:
        subscription_is_active = has_active_subscription(base_url, user_id)
        context['subscription_is_active'] = subscription_is_active
    except Exception as e:
        context['subscription_error'] = str(e)

    # Add recent payments to the context
    try:
        recent_payments = get_recent_payments(base_url, user_id)
        context['payments'] = recent_payments
    except Exception as e:
        context['payments_error'] = str(e)

    # Add calculations to the context
    try:
        calculations = get_calculations(base_url, username)
        context['calculations'] = calculations
    except Exception as e:
        context['calculations_error'] = str(e)

    print(str(context))
    return render(request, template, context)
