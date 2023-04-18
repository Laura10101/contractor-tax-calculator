from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import json
from .services import get_all_jurisdictions, create_jurisdiction

# Create request handler method for jurisdiction requests
@csrf_exempt
def handle_jurisdiction_request(request):
    print(str(request.method))
    if request.method == 'GET':
        response = get_jurisdictions(request)
    elif request.method == 'POST':
        response = create_jurisdiction(json.loads(request.body))
    return JsonResponse(response, safe=False)

# Create your views here.
# Create the controller method to retrieve jurisdictions
def get_jurisdictions(request):
    # First, return all jurisdictions from the Django model
    jurisdictions = get_all_jurisdictions()
    # Now to translate this into JSON data
    serialized_data = serialize('json', jurisdictions)
    # Package the JSON data up into a response object
    response = { 'jurisdictions' : json.loads(serialized_data) }
    # Sending the Json response back to the client
    return response

# Create controller method to create new jurisdiction 
def post_jurisdiction(request):
    # Extract jurisdiction name from http request 
    name = request['name']
    # Call services method to create new jurisdiction
    jurisdiction_id = create_jurisdiction(name)
    # Build JSON response including new jurisdiction ID
    response = { 'jurisdiction_id' : jurisdiction_id }
    # Send the response 
    return response