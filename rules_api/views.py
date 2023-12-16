from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
            'ordinal',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        jurisdiction_id = request.data['jurisdiction_id']
        tax_category_id = request.data['tax_category_id']
        ordinal = request.data['ordinal']
        # Invoke service method 
        try:
            ruleset_id = create_ruleset(jurisdiction_id, tax_category_id, ordinal)
        except ValidationError as e:
            if str(e) == 'A rule already exists with for this tax category in this jurisdiction':
                return Response(
                    { 'error': str(e) },
                    status=status.HTTP_409_CONFLICT
                )
            else:
                return Response(
                    { 'error' : str(e) },
                    status=status.HTTP_400_BAD_REQUEST
                    )
        except TaxCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
                )
        # Create response 
        response = { 'ruleset_id' : ruleset_id }
        # Return response 
        return Response(response)

# Create django rest rule set detail view 
# Django rest views are classes inheriting APIView 
class RuleSetDetail(APIView):
    def delete(self, request, pk):
        # Call apropriate services method
        delete_ruleset(pk)
        # Create response via empty JSON object
        response = { }
        # Return response 
        return Response(response)

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
        # Extract data required for service method 
        name = request.data['name']
        # Invoke service method 
        tax_category_id = create_tax_category(name)
        # Create response 
        response = { 'tax_category_id' : tax_category_id }
        # Return response 
        return Response(response)

# Create django rest tax categories detail view 
# Django rest views are classes inheriting APIView 
class TaxCategoryDetail(APIView):
    def delete(self, request, pk):
        # Call apropriate services method
        delete_tax_category(pk)
        # Create response via empty JSON object
        response = { }
        # Return response 
        return Response(response)

# Create Django REST rules list view
class RuleList(APIView):
    def post(self, request, ruleset_pk):
        # Define the list of required attributes 
        required_attributes = [
            'type',
            'name',
            'ordinal',
            'variable_name',
            'explainer'
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        rule_type = request.data['type']
        name = request.data['name']
        ordinal = request.data['ordinal']
        variable_name = request.data['variable_name']
        explainer = request.data['explainer']
        # Invoke service method
        if rule_type not in ['flat_rate', 'tiered_rate', 'secondary_tiered_rate']:
            return Response(
                { 'error' : 'Invalid request. Please provide a valid rule type.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        try:
            if rule_type == 'flat_rate':
                rule_id = self.__post_flat_rate_rule(ruleset_pk, name, ordinal, variable_name, explainer, request)
            elif rule_type == 'tiered_rate':
                rule_id = create_tiered_rate_rule(ruleset_pk, name, ordinal, variable_name, explainer)
            elif rule_type == 'secondary_tiered_rate':
                rule_id = self.__post_secondary_tiered_rate_rule(ruleset_pk, name, ordinal, variable_name, explainer, request)
        except ValidationError as e:
            return Response(
                { 'error': str(e) },
                status=status.HTTP_400_BAD_REQUEST
            )
        except RuleSet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Generate and return response         
        response = { 'rule_id': rule_id }
        return Response(response)
    
    def __post_flat_rate_rule(self, ruleset_pk, name, ordinal, variable_name, explainer, request):
        # Valid that request contains additional required attributes
        required_attributes = ['tax_rate']
        if not contains_required_attributes(request, required_attributes):
            raise ValidationError('tax_rate is a required attribute')
        
        # Extract additional variables from request
        tax_rate = request.data['tax_rate']
        # Invoke service method
        rule_id = create_flat_rate_rule(name, ruleset_pk, ordinal, variable_name, explainer, tax_rate)
        # Return ID
        return rule_id

    def __post_secondary_tiered_rate_rule(self, ruleset_pk, name, ordinal, variable_name, explainer, request):
        # Valid that request contains additional required attributes
        required_attributes = ['primary_rule_id']
        if not contains_required_attributes(request, required_attributes):
            raise ValidationError('primary_rule_id is a required attribute')
        
        # Extract additional variables from request
        primary_rule_id = request.data['primary_rule_id']
        # Invoke service method
        rule_id = create_flat_rate_rule(ruleset_pk, primary_rule_id, name, ordinal, variable_name, explainer)
        # Return ID
        return rule_id

# Create Django REST rule detail view
class RuleDetail(APIView):
    def delete(self, request, ruleset_pk, pk):
        # Call apropriate services method
        delete_rule(pk)
        # Create response via empty JSON object
        response = { }
        # Return response 
        return Response(response)

    def put(self, request, ruleset_pk, pk):
        # Define the list of required attributes 
        required_attributes = [
            'type',
            'name',
            'ordinal',
            'variable_name',
            'explainer'
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        rule_type = request.data['type']
        name = request.data['name']
        ordinal = request.data['ordinal']
        variable_name = request.data['variable_name']
        explainer = request.data['explainer']
        # Invoke service method
        if rule_type not in ['flat_rate', 'tiered_rate', 'secondary_tiered_rate']:
            return Response(
                { 'error' : 'Invalid request. Please provide a valid rule type.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        try:
            if rule_type == 'flat_rate':
                self.___put_flat_rate_rule(request, pk, name, ordinal, variable_name, explainer)
            elif rule_type == 'tiered_rate':
                update_tiered_rate_rule(pk, name, ordinal, variable_name, explainer)
            elif rule_type == 'secondary_tiered_rate':
                update_secondary_tiered_rate_rule(pk, name, ordinal, variable_name, explainer)
        except ValidationError as e:
            return Response(
                { 'error' : str(e) },
                status=status.HTTP_400_BAD_REQUEST
                )
        except FlatRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TieredRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except SecondaryTieredRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Generate and return response 
        response = { }
        # Return response 
        return Response(response)

    def ___put_flat_rate_rule(self, request, pk, name, ordinal, variable_name, explainer):
        # Valid that request contains additional required attributes
        required_attributes = ['tax_rate']
        if not contains_required_attributes(request, required_attributes):
            raise ValidationError('tax_rate is a required attribute')
        
        # Extract additional variables from request
        tax_rate = request.data['tax_rate']
        update_flat_rate_rule(
            name,
            ordinal,
            explainer,
            variable_name, tax_rate
        )

# Create django rest rule tiers list view 
# Django rest views are classes inheriting APIView 
class RuleTiersList(APIView):
    def post(self, request, ruleset_pk, rule_pk):
        # Define the list of required attributes 
        required_attributes = [
            'min_value',
            'max_value',
            'ordinal',
            'tax_rate',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method
        min_value = request.data['min_value']
        max_value = request.data['max_value']
        ordinal = request.data['ordinal']
        tax_rate = request.data['tax_rate'] 
        # Invoke service method 
        rule_tier_id = create_rule_tier(
            rule_pk,
            min_value,
            max_value,
            ordinal,
            tax_rate
        )
        # Create response 
        response = { 'tier_id' : rule_tier_id }
        # Return response 
        return Response(response)

# Create django rest rule tier detail view 
# Django rest views are classes inheriting APIView 
class RuleTierDetail(APIView):
    def delete(self, request, ruleset_pk, rule_pk, pk):
        # Call apropriate services method
        delete_rule_tier(pk)
        # Create response via empty JSON object
        response = { }
        # Return response 
        return Response(response)

    def put(self, request, ruleset_pk, rule_pk, pk):
        # Define the list of required attributes 
        required_attributes = [
            'min_value',
            'max_value',
            'ordinal',
            'tax_rate',
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        min_value = request.data['min_value']
        max_value = request.data['max_value']
        ordinal = request.data['ordinal']
        tax_rate = request.data['tax_rate']
        # Invoke service method 
        update_rule_tier(pk, min_value, max_value, ordinal, tax_rate)
        # Generate and return response 
        response = { }
        # Return response 
        return Response(response)

# Create django rest secondary rule tiers list view 
# Django rest views are classes inheriting APIView 
class SecondaryRuleTiersList(APIView):
    def post(self, request, ruleset_pk, rule_pk):
        # Define the list of required attributes 
        required_attributes = [
            'primary_tier_id',
            'tax_rate'
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        primary_tier_id = request.data['primary_tier_id']
        tax_rate = request.data['tax_rate']
        # Invoke service method 
        secondary_tier_id = create_secondary_rule_tier(
            primary_tier_id,
            rule_pk,
            tax_rate
        )
        # Generate and return response 
        response = { 'secondary_tier_id' : secondary_tier_id }
        # Return response 
        return Response(response)

# Create django rest secondary rule tier detail view 
# Django rest views are classes inheriting APIView 
class SecondaryRuleTierDetail(APIView):
    def delete(self, request, ruleset_pk, rule_pk, pk):
        # Call apropriate services method
        delete_secondary_rule_tier(pk)
        # Create response via empty JSON object
        response = { }
        # Return response 
        return Response(response)

    def put(self, request, ruleset_pk, rule_pk, pk):
        # Define the list of required attributes 
        required_attributes = [
            'tax_rate'
        ]
        # Validate data 
        if not contains_required_attributes(request, required_attributes):
            return Response(
                { 'error' : 'Invalid request. Please supply all required attributes.' },
                status=status.HTTP_400_BAD_REQUEST
                )
        # Extract data required for service method 
        tax_rate = request.data['tax_rate']
        # Invoke service method 
        update_secondary_rule_tier(pk, tax_rate)
        # Generate and return response 
        response = { }
        # Return response 
        return Response(response)
