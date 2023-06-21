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
    return data

# Create helper function to return form data based on a list of jurisdiction IDs 
def get_forms_by_jurisdiction_ids(url, jurisdiction_ids):
    url = url + '?ids=' + ','.join(str(id) for id in jurisdiction_ids)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Received status code of ' + str(response.status_code) + ' when retrieving forms.')

    data = json.loads(response.text)
    return data
