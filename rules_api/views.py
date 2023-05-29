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

# Create your views here.

# Create django rest rule sets list view 
# Django rest views are classes inheriting APIView 
class RuleSetsList(APIView):
    def post(self, request):
        # Validate data 
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

    def put(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest tax categories list view 
# Django rest views are classes inheriting APIView 
class TaxCategoriesList(APIView):
    def post(self, request):
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

    def put(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest flat rate rules list view 
# Django rest views are classes inheriting APIView 
class FlatRateRulesList(APIView):
    def post(self, request):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest flat rate rule detail view 
# Django rest views are classes inheriting APIView 
class FlatRateRuleDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

    def put(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest tiered rate rule list view 
# Django rest views are classes inheriting APIView 
class TieredRateRulesList(APIView):
    def post(self, request):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest tiered rate rule detail view 
# Django rest views are classes inheriting APIView 
class TieredRateRuleDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

    def put(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest rule tiers list view 
# Django rest views are classes inheriting APIView 
class RuleTiersList(APIView):
    def post(self, request):
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
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest secondary tiered rate rules list view 
# Django rest views are classes inheriting APIView 
class SecondaryTieredRateRulesList(APIView):
    def post(self, request):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest secondary tiered rate detail view 
# Django rest views are classes inheriting APIView 
class SecondaryTieredRateRuleDetail(APIView):
    def delete(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

    def put(self, request, pk):
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass

# Create django rest secondary rule tiers list view 
# Django rest views are classes inheriting APIView 
class SecondaryRuleTiersList(APIView):
    def post(self, request):
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
        # Validate data 
        # Extract data required for service method 
        # Invoke service method 
        # Generate and return response 
        pass
