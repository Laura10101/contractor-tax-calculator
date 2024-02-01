import requests
import json

def get_jurisdictions_by_ids(url, ids=None):
    if ids is not None:
        url = url + '?ids=' + ','.join(str(id) for id in ids)

    response = requests.get(url)

    if response.status_code == 404:
        raise Exception('Jurisdictions could not be found for some of the provided jurisdiction IDs')
    else:
        try:
            data = json.loads(response.text)
        except:
            raise Exception('Failed to retrieve some jurisdictions for the provided jurisdiction IDs')
        
        if 'error' in data:
                raise Exception(data['error'])
                
    return data['jurisdictions']

def has_active_subscription(base_url, user_id):
    url = base_url + '/api/subscriptions/status/?user_id=' + str(user_id)
    response = requests.get(url)
    if response.status_code == 404:
        return false
    else:
        try:
            data = json.loads(response.text)
        except Exception as e:
            print(str(e))
            raise Exception('Failed to check your user subscription status with response code ' + str(response.status_code))
        
        if 'error' in data:
            raise Exception('Failed to check your user subscription status with error: ' + data['error'])
    
    return data['has_active_subscription']

def get_recent_payments(base_url, user_id):
    url = base_url + '/api/payments/?user_id=' + str(user_id)
    response = requests.get(url)
    if response.status_code == 404:
        return []
    else:
        try:
            data = json.loads(response.text)
        except Exception as e:
            print(str(e))
            raise Exception('Failed to retrieve your recent payments with status with response code ' + str(response.status_code))
        
        if 'error' in data:
            raise Exception('Failed to retrieve your recent payments with error: ' + data['error'])
    
    return data

def get_calculations(base_url, username):
    url = base_url + '/api/rules/calculations/?username=' + username
    response = requests.get(url)
    if response.status_code == 404:
        return []
    else:
        try:
            data = json.loads(response.text)
        except:
            raise Exception('Failed to retrieve your calculations with status with response code ' + str(response.status_code))
        
        if 'error' in data:
            raise Exception('Failed to retrieve your calculations with error: ' + data['error'])

    # We need the details of the jurisdictions
    jurisdiction_ids = []
    for calculation in data:
        for jurisdiction_id_as_str, jurisdiction_result in calculation['jurisdictions'].items():
            jurisdiction_ids.append(int(jurisdiction_id_as_str))
    
    # De-duplicate the list of jurisdiction_ids
    # Taken from: https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    jurisdiction_ids = list(dict.fromkeys(jurisdiction_ids))
    print('jurisdiction_ids: ' + str(jurisdiction_ids))
    jurisdictions = get_jurisdictions_by_ids(base_url + '/api/jurisdictions/', jurisdiction_ids)

    # Now generate simplfiied calculation objects in the form { id, date_created, jurisdiction_names }
    calculations = []
    # Iterate over calculations
    for calculation in data:
        # Create the calculation summary object
        calculation_sumnmary = { 'id': calculation['calculation_id'], 'created_date': calculation['created'], 'jurisdictions': [] }
        # Find the jurisdiction name for each jurisdiction in the calculation
        for jurisdiction_id_as_str, jurisdiction in calculation['jurisdictions'].items():
            jurisdiction_id = int(jurisdiction_id_as_str)
            jurisdiction_name = 'Deleted Jurisdiction ' +  str(jurisdiction_id)
            for jurisdiction in jurisdictions:
                if jurisdiction['id'] == jurisdiction_id:
                    jurisdiction_name = jurisdiction['name']
            calculation_sumnmary['jurisdictions'].append(jurisdiction_name)
        
        calculations.append(calculation_sumnmary)
    
    return calculations