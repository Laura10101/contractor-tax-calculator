from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from .services import get_all_jurisdictions, create_jurisdiction

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

# Create controller method to create new jurisdiction 
def post_jurisdiction(request):
    # Extract jurisdiction name from http request 
    name = request.POST.get('name')
    # Call services method to create new jurisdiction
    jurisdiction_id = create_jurisdiction(name)
    # Build JSON response including new jurisdiction ID
    response = { 'jurisdiction_id' : jurisdiction_id }
    # Send the response 
    return JsonResponse(response)