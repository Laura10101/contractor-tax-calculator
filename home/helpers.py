"""Helper functions for home app views."""

import requests
import json


def get_jurisdictions_by_ids(url, ids=None):
    """Retrieve jurisdictions data based on a list of IDs."""

    # Convert the list of IDs into a query string
    if ids is not None:
        url = url + '?ids=' + ','.join(str(id) for id in ids)

    # Retrieve the jurisdictions data
    response = requests.get(url)

    # Raise an error if the response is not found
    if response.status_code == 404:
        raise Exception(
            'Jurisdictions could not be found for ' +
            'some of the provided jurisdiction IDs'
        )
    else:
        # Otherwise, try to parse the response
        # If this fails, raise an error
        try:
            data = json.loads(response.text)
        except Exception:
            raise Exception(
                'Failed to retrieve some jurisdictions for the ' +
                ' provided jurisdiction IDs'
            )

        # If the response contains an error,
        # raise this as an exception
        if 'error' in data:
            raise Exception(data['error'])

    return data['jurisdictions']


def has_active_subscription(base_url, user_id):
    """Check if the user has an active subscription."""

    # Request the user subscription details
    url = base_url + '/api/subscriptions/status/?user_id=' + str(user_id)
    response = requests.get(url)

    # If the response is not found, return false
    if response.status_code == 404:
        return False
    else:
        # Try to parse the response and if that fails
        # raise an exception
        try:
            data = json.loads(response.text)
        except Exception as e:
            print(str(e))
            raise Exception(
                'Failed to check your user subscription status with '
                + ' response code ' + str(response.status_code)
            )

        # If there is an error in the response then
        # raise an exception
        if 'error' in data:
            raise Exception(
                'Failed to check your user subscription status with error: '
                + data['error']
            )

    return data['has_active_subscription']


def get_recent_payments(base_url, user_id):
    """Return the five most recent payments for the user."""

    # Request payments for the user
    url = base_url + '/api/payments/?user_id=' + str(user_id)
    response = requests.get(url)

    # Return an empty list if the response is not found
    if response.status_code == 404:
        return []
    else:
        # Try parsing the response and if that fails,
        # raise an exception
        try:
            data = json.loads(response.text)
        except Exception as e:
            raise Exception(
                'Failed to retrieve your recent payments with ' +
                ' status with response code ' +
                str(response.status_code)
            )

        # If there is an error in the response,
        # raise an exception
        if 'error' in data:
            raise Exception(
                'Failed to retrieve your recent payments ' +
                'with error: ' + data['error']
            )

    return data


def get_calculations(base_url, username):
    """Return a list of calculations for the given user."""

    # Request calculations from the API
    url = base_url + '/api/rules/calculations/?username=' + username
    response = requests.get(url)

    # If the response is not found, return an empty list
    if response.status_code == 404:
        return []
    else:
        # Otherwise, try to parse the response and if that fails,
        # raise an exception
        try:
            data = json.loads(response.text)
        except Exception:
            raise Exception(
                'Failed to retrieve your calculations with status' +
                ' with response code ' + str(response.status_code)
            )

        # If an error is found in the response, raise an error
        if 'error' in data:
            raise Exception(
                'Failed to retrieve your calculations' +
                ' with error: ' + data['error']
            )

    # We need the details of the jurisdictions
    jurisdiction_ids = []
    for calculation in data:
        calculation_items = calculation['jurisdictions'].items()
        for jurisdiction_id_as_str, jurisdiction_result in calculation_items:
            jurisdiction_ids.append(int(jurisdiction_id_as_str))

    # De-duplicate the list of jurisdiction_ids
    # https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    jurisdiction_ids = list(dict.fromkeys(jurisdiction_ids))
    print('jurisdiction_ids: ' + str(jurisdiction_ids))
    jurisdictions = get_jurisdictions_by_ids(
        base_url + '/api/jurisdictions/', jurisdiction_ids
    )

    # Now generate simplfiied calculation objects in the form
    # { id, date_created, jurisdiction_names }
    calculations = []
    # Iterate over calculations
    for calculation in data:
        # Create the calculation summary object
        calculation_sumnmary = {
            'id': calculation['calculation_id'],
            'created_date': calculation['created'],
            'jurisdictions': []
        }
        # Find the jurisdiction name for each jurisdiction in the calculation
        calculation_items = calculation['jurisdictions'].items()
        for jurisdiction_id_as_str, jurisdiction in calculation_items:
            jurisdiction_id = int(jurisdiction_id_as_str)
            jurisdiction_name = 'Deleted Jurisdiction ' + str(jurisdiction_id)
            for jurisdiction in jurisdictions:
                if jurisdiction['id'] == jurisdiction_id:
                    jurisdiction_name = jurisdiction['name']
            calculation_sumnmary['jurisdictions'].append(jurisdiction_name)

        calculations.append(calculation_sumnmary)

    return calculations
