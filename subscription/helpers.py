# Context processor to check user subscription status 
from django.conf import settings
import requests
import json

def user_has_subscription(request):
    base_url = request.scheme + '://' + request.get_host()
    url = base_url + '/api/subscriptions/status/'
    print('Checking the user: ' + str(request.user))
    user_has_subscription = False
    if not str(request.user) == 'AnonymousUser':
        user_id = request.user.id
        response = requests.get(url + '?user_id=' + str(user_id))
        print(response)
        data = json.loads(response.text)
        user_has_subscription = data['has_active_subscription']
    return user_has_subscription
