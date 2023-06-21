import requests
import json

# Create helper functions 
# Create helper function to return details of jurisdictions based on a list of IDs
def get_jurisdictions_by_ids(url, ids):
    url = url + '?ids=' + ids.join(',')
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Create helper function to return form data based on a list of jurisdiction IDs 
def get_forms_by_jurisdiction_ids(url, jurisdiction_ids):
    url = url + '?ids=' + ids.join(',')
    response = requests.get(url)
    data = json.loads(response.text)
    return data
