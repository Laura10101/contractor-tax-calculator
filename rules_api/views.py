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

# Create a function to validate that a request contains
# the required attributes, so the API views can use it
def contains_required_attributes(request, required_attributes):
    for attribute in required_attributes:
            if attribute not in request.data.keys():
                return False
    return True
    
# Create your views here.

# Create django rest rule sets list view 
# Django rest views are classes inheriting APIView 
class RuleSetsList(APIView):
    def post(self, request):
        # Define the list of required attributes 
        required_attributes = [
            'jurisdiction_id',
            'tax_category_id',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest rule set detail view 
# Django rest views are classes inheriting APIView 
class RuleSetDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest tax categories list view 
# Django rest views are classes inheriting APIView 
class TaxCategoriesList(APIView):
    def post(self, request):
        # Define the list of required attributes 
        required_attributes = [
            'name'
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest tax categories detail view 
# Django rest views are classes inheriting APIView 
class TaxCategoryDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create Django REST rules list view
class RuleList(APIView):
    def post(self, request):
        # Define the list of required attributes 
        required_attributes = [
            
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create Django REST rule detail view
class RuleDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

    def put(self, request, pk):
        # Define the list of required attributes 
        required_attributes = [
            
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest rule tiers list view 
# Django rest views are classes inheriting APIView 
class RuleTiersList(APIView):
    def post(self, request):
        # Define the list of required attributes 
        required_attributes = [
            
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest rule tier detail view 
# Django rest views are classes inheriting APIView 
class RuleTierDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

    def put(self, request, pk):
        # Define the list of required attributes 
        required_attributes = [
            
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest secondary rule tiers list view 
# Django rest views are classes inheriting APIView 
class SecondaryRuleTiersList(APIView):
    def post(self, request):
        # Define the list of required attributes 
        required_attributes = [
            
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest secondary rule tier detail view 
# Django rest views are classes inheriting APIView 
class SecondaryRuleTierDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

    def put(self, request, pk):
        # Define the list of required attributes 
        required_attributes = [
            
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass
