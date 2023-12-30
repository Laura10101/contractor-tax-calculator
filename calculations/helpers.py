import requests
import json

# Create helper functions 
# Create helper function to return details of jurisdictions based on a list of IDs
def get_jurisdictions_by_ids(url, ids):
    url = url + '?ids=' + ','.join(str(id) for id in ids)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Received status code of ' + str(response.status_code) + ' when retrieving jurisdictions.')

    data = json.loads(response.text)
    return data['jurisdictions']

# Create helper function to return form data based on a list of jurisdiction IDs 
def get_forms_by_jurisdiction_ids(url, jurisdiction_ids):
    url = url + '?jurisdiction_ids=' + ','.join(str(id) for id in jurisdiction_ids)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Received status code of ' + str(response.status_code) + ' when retrieving forms.')

    data = json.loads(response.text)

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
        print(key)
        if not key == 'csrfmiddlewaretoken':
            if key == 'jurisdiction_ids':
                body['jurisdiction_ids'] = [int(id) for id in request.POST[key].split(',')]
            else:
                body['variables'][key] = cast(request.POST[key])

    print(body)
    response = requests.post(url, json=body)
    if response.ok:
        print(json.loads(response.text))
        return json.loads(response.text)
    else:
        print(json.loads(response.text))
        raise Exception('Posting calculation failed with status code=' + str(response.status_code) + ' and error = ' + json.loads(response.text)['error'])
    

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