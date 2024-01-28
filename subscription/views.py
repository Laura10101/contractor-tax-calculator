from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
import json

from .helpers import user_has_subscription

# Create your views here.
@login_required
def subscription(request):
    if user_has_subscription(request):
        template = 'subscription/subscription_active.html'
        context = {}
    else:
        # List subscription options
        base_url = request.scheme + '://' + request.get_host()
        url = base_url + '/api/subscriptions/options'

        response = requests.get(url)
        print('Response text' + response.text)
        data = json.loads(response.text)

        template = 'subscription/subscription.html'
        context = {
            'subscription_options': data['subscription_options']
        }

    return render(request, template, context)