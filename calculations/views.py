from django.shortcuts import render
from django.urls import reverse
from django.http import Response

from .helpers import *

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
    if request.method != 'POST':
        return Response('This view is only accessible via the select jurisdictions form.', status=400)

    template = 'calculations/calculation_form.html'
    jurisdictions_url = request.build_absolute_uri(reverse('jurisdictions'))
    forms_url = request.build_absolute_uri(reverse('forms'))
    # Generate jurisdiction id list 
    selected_jurisdictions_ids = request.POST.getlist("jurisdictions")
    ids = []
    for jurisdiction_id in selected_jurisdictions_ids:
        ids.append(int(jurisdiction_id))
    # Use helper function to get jurisdiction data 
    jurisdictions = get_jurisdictions_by_ids(jurisdictions_url, ids)
    # Use helper function to get forms data
    forms = get_forms_by_jurisdiction_ids(forms_url, ids)
    # Context is used to pass data into the template 
    context = { 
        'jurisdiction': jurisdictions,
        'forms': forms,
    }
    return render(request, template, context)

    