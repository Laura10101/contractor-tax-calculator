from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from .services import get_all_jurisdictions

# Create your views here.
# Create the controller method to retrieve jurisdictions
def get_jurisdictions(request):
    # First, return all jurisdictions from the Django model
    jurisdictions = get_all_jurisdictions()
    # Now to translate this into JSON data
    serialized_data = serialize('json', jurisdictions.values())
    # Package the JSON data up into a response object
    response = { 'jurisdictions' : json.loads(serialized_data) }
    # Sending the Json response back to the client
    return JsonResponse(response)