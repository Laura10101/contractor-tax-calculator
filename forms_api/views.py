from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import json
from .services import *

# Create request handler method for forms requests
@csrf_exempt
def handle_forms_request(request):
    print(str(request.method))
    if request.method == 'GET':
        response = get_form(request)
    elif request.method == 'POST':
        response = post_form(json.loads(request.body))
    elif request.method == 'DELETE':
        response = delete_form(request)
    return JsonResponse(response, safe=False)

# Create request handler method for questions requests
@csrf_exempt
def handle_questions_request(request):
    print(str(request.method))
    if request.method == 'GET':
        response = get_question(request)
    elif request.method == 'POST':
        response = post_question(json.loads(request.body))
    elif request.method == 'DELETE':
        response = delete_question(request)
    elif request.method == 'PUT':
        response = put_question(json.loads(request.body))
    return JsonResponse(response, safe=False)

# Controller methods
# Process GET requests for forms 
def get_form(request):
    # Extract relevant data from http request 
    # Services method expects a list of jurisdiction ids
    # List of jurisdiction ids will be provded as comma separated list in query string
    # Get value of ids parameter from http request (query string)
    id_string = request.GET['ids']
    # Split string into array of strings 
    id_strings = id_string.split(',')
    # Parse the array of string values into an array integers 
    id_ints = list(map(int, id_strings))
    # Call apropriate services method
    # Create variable to contain results of get method 
    forms = get_forms_by_jurisdiction_ids(id_ints)
    # Create response 
    # Now to translate this into JSON data
    serialized_data = serialize('json', forms)
    # Package the JSON data up into a response object
    response = { 'forms' : json.loads(serialized_data) }
    # Sending the Json response back to the client
    return response

# Process CREATE requests for forms 
def post_form(request):
    pass
    # Extract relevant data from http request 

    # Call apropriate services method

    # Create response 

    # Return response 

# Process DELETE requests for forms
def delete_form(request):
    pass
    # Extract relevant data from http request 

    # Call apropriate services method

    # Create response 

    # Return response 

# Process CREATE requests for questions 
def post_question(request):
    pass
    # Extract relevant data from http request 

    # Call apropriate services method

    # Create response 

    # Return response 

# Process DELETE requests for questions 
def delete_question(request):
    pass
    # Extract relevant data from http request 
    # Call apropriate services method

    # Create response 

    # Return response 

# Process PUT requests for questions 
def put_question(request):
    pass
    # Extract relevant data from http request 

    # Call apropriate services method

    # Create response 

    # Return response 