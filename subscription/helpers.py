"""Define helper methods for subscription app views."""

from django.conf import settings
import requests
import json


def user_has_subscription(request):
    """Check whether or not a user has an active subscription."""

    base_url = request.scheme + '://' + request.get_host()
    url = base_url + '/api/subscriptions/status/'
    user_has_subscription = False
    if not str(request.user) == 'AnonymousUser':
        user_id = request.user.id
        response = requests.get(url + '?user_id=' + str(user_id))
        data = json.loads(response.text)
        user_has_subscription = data['has_active_subscription']
    return user_has_subscription
