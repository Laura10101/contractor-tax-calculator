from subscription.helpers import user_has_subscription
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import SuspiciousOperation


from .helpers import *

import requests
import json

from django.template.defaulttags import register

# Custom filter to return a dictionary item based on its key
# Copied from this StackOverflow answer:
# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable/8000091#8000091
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def length(list):
    return len(list)

# Create your views here.
# Create view for select jurisdictions form 
def select_jurisdictions(request):
    if not user_has_subscription(request):
        return redirect('subscription')
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
        raise SuspiciousOperation("Invalid request. This view is only accessible via the select jurisdictions form.")


    template = 'calculations/calculation_form.html'
    jurisdictions_url = request.build_absolute_uri(reverse('jurisdictions'))
    forms_url = request.build_absolute_uri(reverse('forms'))
    # Generate jurisdiction id list 
    selected_jurisdictions_ids = request.POST.getlist("jurisdictions")
    # Always include the global jurisdiction as the first in the list
    ids = [1]
    for jurisdiction_id in selected_jurisdictions_ids:
        ids.append(int(jurisdiction_id))
    # Use helper function to get jurisdiction data 
    jurisdictions = get_jurisdictions_by_ids(jurisdictions_url, ids)
    print('Jurisdictions data: ' + str(jurisdictions))
    # Use helper function to get forms data
    forms = get_forms_by_jurisdiction_ids(forms_url, ids)
    print('Forms data: ' + str(forms))
    # Context is used to pass data into the template 
    context = { 
        'jurisdictions': jurisdictions,
        'forms': forms,
    }
    return render(request, template, context)

# Create view for displaying the results of the user's tax calculation
# This will use the calculation results template
def display_calculation(request):
    template = 'calculations/calculation_results.html'
    # If the method is POST, then first create the calculation using the
    # rules API
    if request.method == 'POST':
        id = create_calculation('', request.POST)
    else:
        if not 'id' in request.GET:
            raise SuspiciousOperation("Invalid request. Please select a calculation to display.")

    # Retrieve the calculation details from the calculation API
    calculation = get_calculation('', id)
    context = {
        'calculation': calculation
    }
    return render(request, template, context)



    