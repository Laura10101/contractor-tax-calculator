# Context processor to check user subscription status 
import requests
import json

def user_has_subscription(request):
    url = 'https://8000-laura10101-contractorta-x36vvy68pn6.ws-eu99.gitpod.io/api/subscriptions/status/'
    user_id = request.user.id
    response = requests.get(url + '?user_id=' + str(user_id))
    data = json.loads(response.text)
    user_has_subscription = data['has_active_subscription']
    return { 
        'user_has_subscription' : user_has_subscription
    }
