from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
import json
from .serializers import *
from .services import *

# Create django rest forms list view 
# Django rest views are classes inheriting APIView 
class FormsList(APIView):
    def post(self, request):
        # Extract relevant data from http request 
        # For a post request, we get the data from the body of the http request
        # Get jurisdiction id from http body 
        # The request parameter is already a python dictionary (see handler method) 
        jurisdiction_id = request['jurisdiction_id']
        # Call apropriate services method
        form_id = create_form(jurisdiction_id)
        # Create response 
        response = { 'form_id' : form_id }
        # Return response 
        return response 

    # Create get form method 
    def get(self, request):
        # Extract relevant data from http request 
        # Services method expects a list of jurisdiction ids
        # List of jurisdiction ids will be provded as comma separated list in query string
        # Get value of ids parameter from http request (query string)
        if 'jurisdiction_ids' not in request.GET.keys():
            # Code to return an HTTP 400 error
            # From: https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django
            return Response(
                { 'error' : 'Invalid request. Please specify jurisdiction IDs' },
                status=status.HTTP_400_BAD_REQUEST
                )
        id_string = request.GET['jurisdiction_ids']
        # Split string into array of strings 
        id_strings = id_string.split(',')
        # Parse the array of string values into an array integers 
        id_ints = list(map(int, id_strings))
        # Call apropriate services method
        # Create variable to contain results of get method 
        forms = get_forms_by_jurisdiction_ids(id_ints)
        # Create response 
        # Now to translate this into JSON data
        serializer = FormSerializer(forms, many=True)
        # Package the JSON data up into a response object
        response = { 'forms' : serializer.data }
        # Sending the Json response back to the client
        return Response(response)

# Create django rest form detail view 
class FormDetail(APIView):
    # Create delete form method 
    def delete(self, request, pk):
        # Extract relevant data from http request 
        pass
        # Call apropriate services method
        
        # Create response 

        # Return response 

# Create django rest form question detail view
class FormQuestionList(APIView):
    def post(self, request, form_pk):
        # Extract relevant data from http request 
        pass
        # Call apropriate services method

        # Create response 

        # Return response 

# Create django rest form questions list 
class FormQuestionsDetail(APIView):
    def delete(self, request, form_pk, pk):
        # Extract relevant data from http request 
        pass
        # Call apropriate services method

        # Create response 

        # Return response 

    def put(self, request, form_pk, pk):
        # Extract relevant data from http request 
        pass
        # Call apropriate services method

        # Create response 

        # Return response 

