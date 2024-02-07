"""Define views for the calculations app."""

from django.contrib.auth.decorators import login_required
from subscription.helpers import user_has_subscription
from django.shortcuts import render, redirect
from django.urls import reverse


from .helpers import (
    get_jurisdictions_by_ids,
    get_forms_by_jurisdiction_ids,
    create_calculation,
    get_calculation,
    get_jurisdiction_calculation_summaries
)


import requests
import json

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    """Create a custom filter to return a dictionary item based on its key."""
    """Copied from this StackOverflow answer"""
    """https://stackoverflow.com/questions/8000022/"""
    """django-template-how-to-look-up-a-dictionary-value-with-a-variable/"""
    """8000091#8000091"""
    return dictionary.get(key)


@register.filter
def length(list):
    """Register a custom filter to return the length of a list."""
    return len(list)


@login_required
def select_jurisdictions(request):
    """Enable users to select the jurisdictions from a list."""
    """The selected jurisdictions will be used to generate"""
    """the tax calculation"""
    # Check that the user has a valid subscritpion
    # If not, redirect them to the subscription page
    if not user_has_subscription(request):
        return redirect('subscription')
    template = 'calculations/select_jurisdictions.html'

    # Get all jurisdictions from the API
    url = request.build_absolute_uri(reverse('jurisdictions'))
    response = requests.get(url)

    # If the jurisdiction request returned not found
    # then display an error to the user
    if response.status_code == 404:
        return render(
            request,
            template,
            {
                'error': 'Failed to retrieve jurisdictions with status 404'
            }
        )

    # Try to parse the jurisdictions response
    # If an error occurs, display an error to the user
    try:
        data = json.loads(response.text)
    except Exception:
        return render(
            request,
            template,
            {
                'error': 'Failed to retrieve jurisdictions with status ' +
                str(response.status_code)
            }
        )

    # If the response contains an error,
    # display it to the user
    if 'error' in data:
        return render(
            request,
            template,
            {
                'error': 'Failed to retrieve jurisdictions with status '
                + data['error']
            }
        )

    # Render the select jurisdictions template
    context = {
        'jurisdictions': data['jurisdictions']
    }
    return render(request, template, context)


@login_required
def display_form(request):
    """Display the financial information forms to the user."""
    """This form captures the financial information which is"""
    """used to generate the tax calculations."""
    template = 'calculations/calculation_form.html'

    if request.method != 'POST':
        return redirect(reverse('select_jurisdictions'))

    try:
        jurisdictions_url = request.build_absolute_uri(
            reverse('jurisdictions')
        )
    except Exception as e:
        return render(
            request,
            template,
            {
                'error': str(e)
            }
        )

    forms_url = request.build_absolute_uri(reverse('forms'))
    # Generate jurisdiction id list
    selected_jurisdictions_ids = request.POST.getlist("jurisdictions")
    # Always include the global jurisdiction as the first in the list
    ids = [1]
    try:
        for jurisdiction_id in selected_jurisdictions_ids:
            ids.append(int(jurisdiction_id))
    except Exception:
        return render(
            request,
            template,
            {
                'error': 'The provided list of jurisdiction ids ' +
                str(selected_jurisdictions_ids) + ' contains invalid ids.'
            }
        )

    # Use helper function to get jurisdiction data
    try:
        jurisdictions = get_jurisdictions_by_ids(jurisdictions_url, ids)
    except Exception as e:
        return render(
            request,
            template,
            {
                'error': str(e)
            }
        )

    # Use helper function to get forms data
    try:
        forms = get_forms_by_jurisdiction_ids(forms_url, ids)
    except Exception as e:
        return render(
            request,
            template,
            {
                'error': str(e)
            }
        )

    print('Forms data: ' + str(forms))
    # Count the number of questions retrieved
    question_count = 0
    for jurisdiction_id, form in forms.items():
        count = len(forms[jurisdiction_id]['questions'])
        question_count = question_count + count

    # Context is used to pass data into the template
    context = {
        'jurisdiction_ids': ",".join(selected_jurisdictions_ids),
        'jurisdictions': jurisdictions,
        'forms': forms,
        "question_count": question_count
    }
    return render(request, template, context)


@login_required
def display_calculation(request):
    """Display tax calculation results."""
    """Supports both POSTing new tax calculations"""
    """and retrieving existing calculations by ID"""
    template = 'calculations/calculation_results.html'
    # If the method is POST, then first create the calculation using the
    # rules API
    if request.method == 'POST':
        try:
            calculation = create_calculation(
                request.build_absolute_uri(reverse('calculations')),
                request
            )
        except Exception as e:
            return render(
                request,
                template,
                {
                    'error': str(e)
                }
            )
    else:
        # Otherwise, retrieve the calculation via the API based on
        # its ID
        if 'id' not in request.GET:
            return redirect(reverse('contractor_home'))
        else:
            id = int(request.GET['id'])
            try:
                calculation = get_calculation(
                    request.build_absolute_uri(reverse('calculations')),
                    id
                )
            except Exception as e:
                return render(
                    request,
                    template,
                    {
                        'error': str(e)
                    }
                )

    summaries, excluded_jurisdictions = get_jurisdiction_calculation_summaries(
        calculation,
        request.build_absolute_uri(reverse('jurisdictions'))
    )
    context = {
        'calculation': calculation,
        'summaries': summaries,
        'excluded_jurisdictions': excluded_jurisdictions,
    }
    return render(request, template, context)
