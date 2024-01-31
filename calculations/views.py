from django.contrib.auth.decorators import login_required
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
@login_required
def select_jurisdictions(request):
    if not user_has_subscription(request):
        return redirect('subscription')
    template = 'calculations/select_jurisdictions.html'
    url = request.build_absolute_uri(reverse('jurisdictions'))
    response = requests.get(url)

    if response.status_code == 404:
        return render(request, template, { 'error': 'Failed to retrieve jurisdictions with status code 404' })

    try:
        data = json.loads(response.text)
    except:
        return render(request, template, { 'error': 'Failed to retrieve jurisdictions with response code ' + str(response.status_code) })
    
    if 'error' in data:
        return render(request, template, { 'error': 'Failed to retrieve jurisdictions with error ' + option_data['error'] })

    context = {
        'jurisdictions': data['jurisdictions']
    }
    return render(request, template, context)

# Create view for displaying financial information form
# This will use the calculation form template 
@login_required
def display_form(request):
    template = 'calculations/calculation_form.html'

    if request.method != 'POST':
        return redirect(reverse('select_jurisdictions'))

    try:
        jurisdictions_url = request.build_absolute_uri(reverse('jurisdictions'))
    except Exception as e:
        return render(request, template, { 'error': str(e)})

    forms_url = request.build_absolute_uri(reverse('forms'))
    # Generate jurisdiction id list 
    selected_jurisdictions_ids = request.POST.getlist("jurisdictions")
    # Always include the global jurisdiction as the first in the list
    ids = [1]
    try:
        for jurisdiction_id in selected_jurisdictions_ids:
            ids.append(int(jurisdiction_id))
    except:
        return render(request, template, { 'error': 'The provided list of jurisdiction ids ' + str(selected_jurisdictions_ids) + ' contains invalid ids.'})

    # Use helper function to get jurisdiction data 
    try:
        jurisdictions = get_jurisdictions_by_ids(jurisdictions_url, ids)
    except Exception as e:
        return render(request, template, { 'error': str(e)})

    print('Jurisdictions data: ' + str(jurisdictions))
    # Use helper function to get forms data
    try:
        forms = get_forms_by_jurisdiction_ids(forms_url, ids)
    except Exception as e:
        return render(request, template, { 'error': str(e)})

    print('Forms data: ' + str(forms))
    # Context is used to pass data into the template 
    context = {
        'jurisdiction_ids': ",".join(selected_jurisdictions_ids),
        'jurisdictions': jurisdictions,
        'forms': forms,
    }
    return render(request, template, context)

# Create view for displaying the results of the user's tax calculation
# This will use the calculation results template
@login_required
def display_calculation(request):
    template = 'calculations/calculation_results.html'
    # If the method is POST, then first create the calculation using the
    # rules API
    if request.method == 'POST':
        try:
            calculation = create_calculation(request.build_absolute_uri(reverse('calculations')), request)
            print(str(calculation))
        except Exception as e:
            return render(request, template, { 'error': str(e)})
    else:
        if not 'id' in request.GET:
            return redirect(reverse('contractor_home'))
        else:
            id = int(request.GET['id'])
            try:
                calculation = get_calculation(request.build_absolute_uri(reverse('calculations')), id)
            except Exception as e:
                return render(request, template, { 'error': str(e)})

    context = {
        'calculation': calculation,
        'summaries': get_jurisdiction_calculation_summaries(calculation, request.build_absolute_uri(reverse('jurisdictions')))
    }
    return render(request, template, context)

