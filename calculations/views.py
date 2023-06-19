from django.shortcuts import render
from django.urls import reverse

import requests
import json

# Create your views here.
def select_jurisdictions(request):
    template = 'calculations/select_jurisdictions.html'
    url = request.build_absolute_uri(reverse('jurisdictions'))
    response = requests.get(url)
    print(response.text)
    data = json.loads(response.text)
    print('Jurisdictions: ' + str(data['jurisdictions']))

    context = {
        'jurisdictions': data['jurisdictions']
    }
    return render(request, template, context)
