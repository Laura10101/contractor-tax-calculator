from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.
def checkout(request):
    template = 'checkout/checkout.html'
    context = { }
    return render(request, template, context)