"""Define view methods for the jurisdictions API."""

from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from .serializers import JurisdictionSerializer
from .services import (
    get_all_jurisdictions,
    create_jurisdiction,
    delete_jurisdictions_by_id,
    get_jurisdictions_by_ids
)


def id_string_to_list(id_string):
    """Convert a comma-separated ID string to a list."""

    # Divide string by commas
    id_strings = id_string.split(',')

    # Parse id strings to integers
    ids = []
    for id_str in id_strings:
        id = int(id_str)
        ids.append(id)
    return ids


class JurisdictionList(APIView):
    """Create JursidictionList API View"""

    # Implement get jurisidctions controller method
    def get(self, request):
        """Return a list of jurisdictions."""
        """Return either all jurisdictions or """
        """jurisdictions matching the specified IDs."""

        # First, return all jurisdictions from the Django model
        if 'ids' in request.GET:
            # Get id string from http request
            id_string = request.GET['ids']

            # Parse each value into an integer
            try:
                ids = id_string_to_list(id_string)
            except ValueError:
                return Response(
                    {
                        'error': 'IDs string is not correctly formatted.'
                    },
                    status=400
                )
            except Exception:
                return Response(
                    {
                        'error': 'A server error occurred.'
                    },
                    status=500
                )
            jurisdictions = get_jurisdictions_by_ids(ids)
        else:
            jurisdictions = get_all_jurisdictions()
        # Create the jurisidction serializer instance to serialize
        # the returned jurisidctions
        serializer = JurisdictionSerializer(jurisdictions, many=True)
        # Package the JSON data up into a response object
        response = {
            'jurisdictions': serializer.data
        }
        # Sending the Json response back to the client
        return Response(response)

    def delete(self, request):
        """Create controller method to delete jurisdictions by ids."""

        # Extract jurisdiction ids to delete
        # Get id string from http request
        id_string = request.GET['ids']

        # Parse each value into an integer
        try:
            ids = id_string_to_list(id_string)
        except ValueError:
            return Response(
                {
                    'error': 'IDs string is not correctly formatted.'
                },
                status=400
            )
        except Exception:
            return Response(
                {
                    'error': 'A server error occurred.'
                },
                status=500
            )
        # Call services method to delete jurisdictions
        delete_jurisdictions_by_id(ids)
        # Build empty JSON response
        response = {}
        # Return response
        return Response(response)

    def post(self, request):
        """Create controller method to create new jurisdiction."""
        # Create the jurisidction serializer instance to serialize
        # the data provided in the request
        serializer = JurisdictionSerializer(data=request.data)
        # Check that the data is valid and raise an exception if not
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Extract the ID and return the response
        return Response(serializer.data)
