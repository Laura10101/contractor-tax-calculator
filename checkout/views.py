from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    template = 'checkout/checkout.html'
    context = { 
        'stripe_public_key': stripe_public_key,
        'client_secret_key': 'intent.client_secret',
    }
    return render(request, template, context)