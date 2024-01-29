import requests
import json

# Create helper functions 
# Create helper function to return details of jurisdictions based on a list of IDs
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

# Create helper function to return form data based on a list of jurisdiction IDs 
def get_forms_by_jurisdiction_ids(url, jurisdiction_ids):
    url = url + '?jurisdiction_ids=' + ','.join(str(id) for id in jurisdiction_ids)
    response = requests.get(url)

    if response.status_code == 404:
        raise Exception('Forms could not be found for some of the provided jurisdiction IDs')
    else:
        try:
            data = json.loads(response.text)
        except:
            raise Exception('Failed to retrieve some forms for the provided jurisdiction IDs')
        
        if 'error' in data:
                raise Exception(data['error'])


    # JSON treats keys as strings so need to cast the keys back to ints
    deserialised_data = {}
    for jurisdiction_id_str in data['forms'].keys():
        deserialised_data[int(jurisdiction_id_str)] = data['forms'][jurisdiction_id_str]
    return deserialised_data

def create_calculation(url, request):
    body = {
        'username': request.user.username,
        'variables': {}
    }
    for key in request.POST:
        if not key == 'csrfmiddlewaretoken':
            if key == 'jurisdiction_ids':
                body['jurisdiction_ids'] = [int(id) for id in request.POST[key].split(',')]
            else:
                body['variables'][key] = cast(request.POST[key])

    response = requests.post(url, json=body)
    if response.status_code == 404:
        raise Exception('Unable to locate rules for some jurisdictions in the provided list of jurisdiction IDs: ' + str(body['jurisdiction_ids']))
    else:
        try:
            data = json.loads(response.text)
        except:
            raise Exception('Failed to create calculation with response code ' + str(response.status_code))
        
        if 'error' in data:
            raise Exception(data['error'])
        else:
            return data
    

def get_calculation(url, id):
    return {}

def cast(value):
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
    for jurisdiction in all_jurisdictions:
        if jurisdiction_id == str(jurisdiction['id']):
            return jurisdiction['name']
    return None

def get_jurisdiction_calculation_summaries(calculation, jurisdictions_url):
    all_jurisdictions = get_jurisdictions_by_ids(jurisdictions_url)
    jurisdictions = {}

    for jurisdiction_id, jurisdiction_results in calculation['jurisdictions'].items():
        jurisdiction_name = find_jurisdiction_name(jurisdiction_id, all_jurisdictions)
        if not jurisdiction_name in jurisdictions:
            jurisdictions[jurisdiction_name] = {
                'jurisdiction_id': jurisdiction_id,
            }

        total = 0.0
        for result in jurisdiction_results:
            tax_category = result['tax_category']
            tax_payable = result['tax_payable']

            if not tax_category in jurisdictions[jurisdiction_name]:
                jurisdictions[jurisdiction_name][tax_category] = 0.0

            jurisdictions[jurisdiction_name][tax_category] += tax_payable

            total += tax_payable

        jurisdictions[jurisdiction_name]['Total'] = total
    return jurisdictions

