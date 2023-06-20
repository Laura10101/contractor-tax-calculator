from django.shortcuts import render
from django.urls import reverse

import requests
import json

# Create your views here.
# Create view for select jurisdictions form 
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

# Create view for displaying financial information form
# This will use the calculation form template 
def display_form(request):
    template = 'calculations/calculation_form.html'
    # Context is used to pass data into the template 
    context = { }
    return render(request, template, context)
    