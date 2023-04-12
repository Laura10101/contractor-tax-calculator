from django.shortcuts import render
from .services import get_all_jurisdictions

# Create your views here.
# Create the controller method to retrieve jurisdictions
def get_jurisdictions():
    jurisdictions = get_all_jurisdictions()
    # Convert into a Python dictionary
    # Django will translate this into a JSON object
    response = { 'jurisdictions' : jurisdictions }
    # Sending the HTTP response, containing the JSON data
    # back to the client
    return HttpResponse(response)