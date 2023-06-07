from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from .serializers import JurisdictionSerializer
from .services import get_all_jurisdictions, create_jurisdiction, delete_jurisdictions_by_id

# Create JursidictionList API View
class JurisdictionList(APIView):

    # Implement get jurisidctions controller method
    def get(self, request):
        # First, return all jurisdictions from the Django model
        jurisdictions = get_all_jurisdictions()
        # Create the jurisidction serializer instance to serialize
        # the returned jurisidctions
        serializer = JurisdictionSerializer(jurisdictions, many=True)
        # Package the JSON data up into a response object
        response = { 'jurisdictions' : serializer.data }
        # Sending the Json response back to the client
        return Response(response)

    # Create controller method to delete jurisdictions by ids
    def delete(self, request):
        # Extract jurisdiction ids to delete 
        # Get id string from http request 
        id_string = request.GET['ids']
        # Divide string by commas 
        id_strings = id_string.split(',')
        # Parse each value into an integer
        try:
            ids = []
            for id_str in id_strings:
                id = int(id_str)
                ids.append(id)
        except ValueError:
            return Response(
                    { 'error' : 'IDs string is not correctly formatted.' },
                    status=400
                    )
        except:
            return Response(
                    { 'error' : 'A server error occurred.' },
                    status=500
                    )
        # Call services method to delete jurisdictions 
        delete_jurisdictions_by_id(ids)
        # Build empty JSON response 
        response = { }
        # Return response 
        return Response(response)


    # Create controller method to create new jurisdiction 
    def post(self, request):
        # Create the jurisidction serializer instance to serialize
        # the data provided in the request
        serializer = JurisdictionSerializer(data=request.data)
        # Check that the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Extract the ID and return the response
        return Response(serializer.data)