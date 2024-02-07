"""Defines helper functoins for calculation views."""

import json
import requests


def get_jurisdictions_by_ids(url, ids=None):
    """Return jurisdictions data for specified IDs."""
    # If the list of IDs is not null then generate the query string
    if ids is not None:
        url = url + '?ids=' + ','.join(str(id) for id in ids)

    # Get jurisdictions data for the query string
    response = requests.get(url)

    # Raise an exception if not found response was returned
    if response.status_code == 404:
        raise Exception(
            'Jurisdictions could not be found' +
            'for some jurisdiction IDs'
        )
    else:
        # Try to parse the json response
        # If this fails, raise an exception
        try:
            data = json.loads(response.text)
        except Exception:
            raise Exception(
                'Failed to retrieve jurisdictions' +
                'for the given IDs'
            )

        # If the response data contains an error,
        # raise an exception
        if 'error' in data:
            raise Exception(data['error'])

    return data['jurisdictions']


# Create helper function to return form data based on a
# list of jurisdiction IDs
def get_forms_by_jurisdiction_ids(url, jurisdiction_ids):
    """Return form and question data based on given jurisdiction IDs."""
    # Generate the jurisdiction ID query string
    id_str = ','.join(str(id) for id in jurisdiction_ids)
    url = url + '?jurisdiction_ids=' + id_str

    # Get the forms data from the forms API
    response = requests.get(url)

    # If the response is not found, raise an exception
    if response.status_code == 404:
        raise Exception(
            'Forms could not be found for some of ' +
            'the provided jurisdiction IDs'
        )
    else:
        # Try and parse the JSON data
        # If this fails, return an exception
        try:
            data = json.loads(response.text)
        except Exception:
            raise Exception(
                'Failed to retrieve some forms for ' +
                'the provided jurisdiction IDs'
            )

        # If the response data includes an error, raise an exception
        if 'error' in data:
            raise Exception(data['error'])

    # JSON treats keys as strings so need to cast the keys back to ints
    deserialised_data = {}
    for jurisdiction_id_str in data['forms'].keys():
        form = data['forms'][jurisdiction_id_str]
        deserialised_data[int(jurisdiction_id_str)] = form
    return deserialised_data


def create_calculation(url, request):
    """Create a new calculation entity via the rules API."""
    body = {
        'username': request.user.username,
        'variables': {}
    }
    # Build the variable table from the submitted form data
    for key in request.POST:
        if not key == 'csrfmiddlewaretoken':
            if key == 'jurisdiction_ids':
                ids = [int(id) for id in request.POST[key].split(',')]
                body['jurisdiction_ids'] = ids
            else:
                body['variables'][key] = cast(request.POST[key])

    # Post the create calculation request
    response = requests.post(url, json=body)

    # If the response is not found, raise an exception
    if response.status_code == 404:
        raise Exception(
            'Unable to locate rules for some jurisdictions in the ' +
            'provided list of jurisdiction IDs: ' +
            str(body['jurisdiction_ids'])
        )
    else:
        # Try to parse response data and if this fails,
        # raise an error
        try:
            data = json.loads(response.text)
        except Exception:
            raise Exception(
                'Failed to create calculation with response code '
                + str(response.status_code)
            )

        # If the response data contains an error,
        # raise an exception
        # Otherwise return the deserialised data
        if 'error' in data:
            raise Exception(data['error'])
        else:
            return data


def get_calculation(url, id):
    """Return a calculation from the rules API based on its ID."""
    # Get the calculation based on its id
    response = requests.get(url + str(id) + '/')

    # If the response is not found, raise an exception
    if response.status_code == 404:
        raise Exception(
            'No calculation could be found for the id ' +
            str(id)
        )
    else:
        # Try and parse the response data
        # If this fails, raise an exception
        try:
            data = json.loads(response.text)
        except Exception:
            raise Exception(
                'Failed to retrieve the calculation with id '
                + str(id) + '.'
            )

        # If the response contains an error,
        # raise an exception
        if 'error' in data:
            raise Exception(data['error'])

    return data


def cast(value):
    """Cast a string value to the correct data type."""
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    else:
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value


def find_jurisdiction_name(jurisdiction_id, all_jurisdictions):
    """Return a jurisdiction name based on the jurisdiction ID."""
    # Loop through the jurisdiction list to find the one that matches
    # the given ID
    for jurisdiction in all_jurisdictions:
        if jurisdiction_id == str(jurisdiction['id']):
            return jurisdiction['name']
    return None


def get_jurisdiction_calculation_summaries(calculation, jurisdictions_url):
    """Generate a calculation summary based on a serialised calculation."""
    # Get all jurisdictions data from the jurisdiction API
    all_jurisdictions = get_jurisdictions_by_ids(jurisdictions_url)

    # Initialise the jurisdiction object
    jurisdictions = {}

    # Parse the list of excluded jurisdiction IDs
    excluded_id_str = calculation['excluded_jurisdiction_ids']
    excluded_jurisdiction_ids = excluded_id_str.split(',')

    # Get an array of jurisdiction names for the given
    # jurisdiction IDs
    excluded_jurisdictions = []
    for id in excluded_jurisdiction_ids:
        try:
            jurisdiction_name = find_jurisdiction_name(
                int(id),
                all_jurisdictions
            )
            if jurisdiction_name is None:
                excluded_jurisdictions.append(
                    'Deleted jurisdiction ' + str(id)
                )
            else:
                excluded_jurisdictions.append(jurisdiction_name)
        except Exception:
            pass

    calculation_rows = calculation['jurisdictions'].items()
    for jurisdiction_id, jurisdiction_results in calculation_rows:
        # Get the jurisdiction name for the current jurisdiction id
        jurisdiction_name = find_jurisdiction_name(
            jurisdiction_id,
            all_jurisdictions
        )
        if jurisdiction_name is None:
            jurisdiction_name = 'Deleted Jurisdiction ' + str(jurisdiction_id)
        if jurisdiction_name not in jurisdictions:
            jurisdictions[jurisdiction_name] = {
                'jurisdiction_id': jurisdiction_id,
            }

        # Structure the calculation results for current jurisdiction
        total = 0.0
        for result in jurisdiction_results:
            tax_category = result['tax_category']
            tax_payable = result['tax_payable']

            if tax_category not in jurisdictions[jurisdiction_name]:
                jurisdictions[jurisdiction_name][tax_category] = 0.0

            jurisdictions[jurisdiction_name][tax_category] += tax_payable

            total += tax_payable

        jurisdictions[jurisdiction_name]['Total'] = total
    return jurisdictions, excluded_jurisdictions
