"""Define view methods for rules API."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import (
    get_rulesets_by_jurisdiction_id,
    create_ruleset,
    update_ruleset_ordinal,
    delete_ruleset,
    delete_rulesets_for_jurisdiction,
    get_tax_categories,
    create_tax_category,
    delete_tax_category,
    delete_rule,
    create_flat_rate_rule,
    update_flat_rate_rule,
    create_tiered_rate_rule,
    update_tiered_rate_rule,
    create_rule_tier,
    update_rule_tier,
    delete_rule_tier,
    create_secondary_tiered_rate_rule,
    update_secondary_tiered_rate_rule,
    create_secondary_rule_tier,
    update_secondary_rule_tier,
    delete_secondary_rule_tier,
    create_calculation,
    get_calculations_for_user,
    get_calculation_by_id
)


def contains_required_attributes(request, required_attributes):
    """Check that the request contains the expected attributes."""

    for attribute in required_attributes:
        if attribute not in request.data.keys():
            return False
    return True


class RuleSetsList(APIView):
    """Create Rulesets List view."""

    def __serialise_rule_tier(self, tier):
        """Serialise a rule tier to JSON."""

        return {
            'id': tier.id,
            'min_value': tier.min_value,
            'max_value': tier.max_value,
            'ordinal': tier.ordinal,
            'tier_rate': tier.tier_rate
        }

    def __serialise_secondary_rule_tier(self, tier):
        """Serialise a secondary rule tier to JSON."""

        return {
            'id': tier.id,
            'tier_rate': tier.tier_rate,
            'ordinal': tier.ordinal,
            'primary_tier_id': tier.primary_tier.id
        }

    def __serialise_rule(self, rule):
        """Serialise a rule to JSON."""

        # Serialise the generic attributes
        serialised_rule = {
            'id': rule.id,
            'name': rule.name,
            'explainer': rule.explainer,
            'ordinal': rule.ordinal,
            'variable_name': rule.variable_name
        }

        # Serialise the specific attributes for the given
        # rule type
        if isinstance(rule, FlatRateRule):
            serialised_rule['type'] = 'flat_rate'
            serialised_rule['tax_rate'] = rule.flat_rate
        else:
            if isinstance(rule, TieredRateRule):
                serialised_rule['type'] = 'tiered_rate'
            elif isinstance(rule, SecondaryTieredRateRule):
                serialised_rule['primary_rule'] = self.__serialise_rule(
                    rule.primary_rule
                )
                serialised_rule['type'] = 'secondary_tiered_rate'

            serialised_rule['tiers'] = []
            for tier in rule.tiers.order_by('ordinal').all():
                if isinstance(rule, TieredRateRule):
                    serialised_rule['tiers'].append(
                        self.__serialise_rule_tier(tier)
                    )
                else:
                    serialised_rule['tiers'].append(
                        self.__serialise_secondary_rule_tier(tier)
                    )

        if isinstance(rule, SecondaryTieredRateRule):
            serialised_rule['primary_rule_id'] = rule.primary_rule.id

        return serialised_rule

    def get(self, request):
        """Return the list of rules for a given jurisdiction."""

        # Validate the request data
        if 'jurisdiction_id' not in request.GET.keys():
            # Code to return an HTTP 400 error
            # https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django
            return Response(
                {
                    'error': 'Invalid request. Please specify jurisdiction ID'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            jurisdiction_id = int(request.GET['jurisdiction_id'])
        except Exception:
            return Response(
                {
                    'error': 'Invalid request. Jurisdiction ID must be an ' +
                    'integer'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Invoke the service method
        rulesets = get_rulesets_by_jurisdiction_id(jurisdiction_id)
        # Serialise the retrieved rulesets
        serialised_rulesets = []
        for ruleset in rulesets:
            serialised_ruleset = {
                'id': ruleset.id,
                'name': str(ruleset),
                'tax_category_id': ruleset.tax_category.id,
                'ordinal': ruleset.ordinal,
                'rules': []
            }
            for rule in ruleset.rules.order_by('ordinal').all():
                serialised_ruleset['rules'].append(self.__serialise_rule(rule))
            serialised_rulesets.append(serialised_ruleset)

        # Return a response
        return Response(serialised_rulesets)

    def post(self, request):
        """Create a new ruleset."""

        # Define the list of required attributes
        required_attributes = [
            'jurisdiction_id',
            'tax_category_id',
            'ordinal',
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        jurisdiction_id = request.data['jurisdiction_id']
        tax_category_id = request.data['tax_category_id']
        ordinal = request.data['ordinal']
        # Invoke service method
        try:
            ruleset_id = create_ruleset(
                jurisdiction_id, tax_category_id, ordinal
            )
        except ValidationError as e:
            conflict_message = 'A ruleset already exists for this tax category'
            conflict_message = conflict_message + ' in this jurisdiction'
            if e.messages[0] == conflict_message:
                return Response(
                    {
                        'error': str(e)
                    },
                    status=status.HTTP_409_CONFLICT
                )
            else:
                return Response(
                    {
                        'error': str(e)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except TaxCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
                )
        # Create response
        response = {
            'ruleset_id': ruleset_id
        }
        # Return response
        return Response(response)


class RuleSetDetail(APIView):
    """Create django rest rule set detail view."""

    def delete(self, request, pk):
        """Delete a ruleset based on its ID."""

        # Call apropriate services method
        try:
            delete_ruleset(pk)
        except RuleSet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Create response via empty JSON object
        response = {}
        # Return response
        return Response(response)

    def patch(self, request, pk):
        """Update an existing ruleset."""

        # Define the list of required attributes
        required_attributes = [
            'ordinal',
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        ordinal = request.data['ordinal']
        # Invoke service method
        try:
            update_ruleset_ordinal(pk, ordinal)
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except RuleSet.DoesNotExist:
            return Response(
                {
                    'error': 'Ruleset with id ' + str(pk) + ' was not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        # Create response
        response = {
            'ruleset_id': pk
        }
        # Return response
        return Response(response)


class TaxCategoriesList(APIView):
    """Create django rest tax categories list view."""

    def get(self, request):
        """Get a list of all tax categories."""

        tax_categories = get_tax_categories()
        serialised_categories = []
        for category in tax_categories:
            serialised_category = {
                'tax_category_id': category.id,
                'name': category.name
            }
            serialised_categories.append(serialised_category)
        return Response(serialised_categories)

    def post(self, request):
        """Create a new tax category."""

        # Define the list of required attributes
        required_attributes = [
            'name'
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        name = request.data['name']
        # Invoke service method
        try:
            tax_category_id = create_tax_category(name)
        except ValidationError as e:
            conflict_message = "{'name': ['Tax category with this "
            conflict_message = conflict_message + "Name already exists.']}"
            if str(e) == conflict_message:
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                return Response(
                    {
                        'error': str(e)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Create response
        response = {
            'tax_category_id': tax_category_id
        }
        # Return response
        return Response(response)


class TaxCategoryDetail(APIView):
    """Create django rest tax categories detail view."""

    def delete(self, request, pk):
        """Delete a tax category based on its ID."""
        # Call apropriate services method
        try:
            delete_tax_category(pk)
        except TaxCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Create response via empty JSON object
        response = {}
        # Return response
        return Response(response)


class RuleList(APIView):
    """Create Django REST rules list view."""

    def post(self, request, ruleset_pk):
        """Create a new rule."""
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
                {
                    'error': 'Invalid request. Please supply all required '
                    + 'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        rule_type = request.data['type']
        name = request.data['name']
        ordinal = request.data['ordinal']
        variable_name = request.data['variable_name']
        explainer = request.data['explainer']
        # Invoke service method
        rule_types = ['flat_rate', 'tiered_rate', 'secondary_tiered_rate']
        if rule_type not in rule_types:
            return Response(
                {
                    'error': 'Invalid request. Please provide a valid rule ' +
                    'type.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if rule_type == 'flat_rate':
                rule_id = self.__post_flat_rate_rule(
                    ruleset_pk,
                    name,
                    ordinal,
                    explainer,
                    variable_name,
                    request
                )
            elif rule_type == 'tiered_rate':
                rule_id = create_tiered_rate_rule(
                    ruleset_pk,
                    name,
                    ordinal,
                    explainer,
                    variable_name
                )
            elif rule_type == 'secondary_tiered_rate':
                rule_id = self.__post_secondary_tiered_rate_rule(
                    ruleset_pk,
                    name,
                    ordinal,
                    explainer,
                    variable_name,
                    request
                )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except RuleSet.DoesNotExist:
            return Response(
                {
                    'error': 'Ruleset with id=' + str(ruleset_pk) +
                    ' was not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except TieredRateRule.DoesNotExist:
            return Response(
                {
                    'error': 'Tiered rate rule with id=' +
                    str(request.data['primary_rule_id']) +
                    ' was not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate and return response
        response = {
            'rule_id': rule_id
        }
        return Response(response)

    def __post_flat_rate_rule(
        self,
        ruleset_pk,
        name,
        ordinal,
        explainer,
        variable_name,
        request
    ):
        """Create a new flat rate rule."""

        # Valid that request contains additional required attributes
        required_attributes = ['tax_rate']
        if not contains_required_attributes(request, required_attributes):
            raise ValidationError('tax_rate is a required attribute')

        # Extract additional variables from request
        tax_rate = request.data['tax_rate']
        # Invoke service method
        rule_id = create_flat_rate_rule(
            ruleset_pk,
            name, ordinal,
            explainer,
            variable_name,
            tax_rate
        )
        # Return ID
        return rule_id

    def __post_secondary_tiered_rate_rule(
        self,
        ruleset_pk,
        name,
        ordinal,
        explainer,
        variable_name,
        request
    ):
        """Create a new secondary tiered rate rule."""

        # Valid that request contains additional required attributes
        required_attributes = ['primary_rule_id']
        if not contains_required_attributes(request, required_attributes):
            raise ValidationError('primary_rule_id is a required attribute')

        # Extract additional variables from request
        primary_rule_id = request.data['primary_rule_id']
        # Invoke service method
        rule_id = create_secondary_tiered_rate_rule(
            ruleset_pk,
            primary_rule_id,
            name,
            ordinal,
            explainer,
            variable_name
        )
        # Return ID
        return rule_id


class RuleDetail(APIView):
    """Create Django REST rule detail view."""

    def delete(self, request, ruleset_pk, pk):
        """Delete a rule based on its ID."""

        # Call apropriate services method
        delete_rule(pk)
        # Create response via empty JSON object
        response = {}
        # Return response
        return Response(response)

    def put(self, request, ruleset_pk, pk):
        """Update a rule based on its ID."""

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
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        rule_type = request.data['type']
        name = request.data['name']
        ordinal = request.data['ordinal']
        variable_name = request.data['variable_name']
        explainer = request.data['explainer']
        # Invoke service method
        rule_types = ['flat_rate', 'tiered_rate', 'secondary_tiered_rate']
        if rule_type not in rule_types:
            return Response(
                {
                    'error': 'Invalid request. Please provide a valid rule ' +
                    'type.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if rule_type == 'flat_rate':
                self.___put_flat_rate_rule(
                    request,
                    pk,
                    name,
                    ordinal,
                    explainer,
                    variable_name
                )
            elif rule_type == 'tiered_rate':
                update_tiered_rate_rule(
                    pk,
                    name,
                    ordinal,
                    explainer,
                    variable_name
                )
            elif rule_type == 'secondary_tiered_rate':
                update_secondary_tiered_rate_rule(
                    pk,
                    name,
                    ordinal,
                    explainer,
                    variable_name
                )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except FlatRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except TieredRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except SecondaryTieredRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Generate and return response
        response = {}
        # Return response
        return Response(response)

    def ___put_flat_rate_rule(
        self,
        request,
        pk,
        name,
        ordinal,
        explainer,
        variable_name
    ):
        """Update an existing flat rate rule."""

        # Valid that request contains additional required attributes
        required_attributes = ['tax_rate']
        if not contains_required_attributes(request, required_attributes):
            raise ValidationError('tax_rate is a required attribute')

        # Extract additional variables from request
        tax_rate = request.data['tax_rate']
        update_flat_rate_rule(
            pk,
            name,
            ordinal,
            explainer,
            variable_name,
            tax_rate
        )


class RuleTiersList(APIView):
    """Create django rest rule tiers list view."""

    def post(self, request, ruleset_pk, rule_pk):
        """Create a new rule tier."""

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
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        min_value = request.data['min_value']
        max_value = request.data['max_value']
        ordinal = request.data['ordinal']
        tax_rate = request.data['tax_rate']
        # Invoke service method
        try:
            rule_tier_id = create_rule_tier(
                rule_pk,
                min_value,
                max_value,
                ordinal,
                tax_rate
            )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except TieredRateRule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Create response
        response = {
            'tier_id': rule_tier_id
        }
        # Return response
        return Response(response)


class RuleTierDetail(APIView):
    """Create django rest rule tier detail view."""

    def delete(self, request, ruleset_pk, rule_pk, pk):
        """Delete a rule tier based on its ID."""

        # Call apropriate services method
        delete_rule_tier(pk)
        # Create response via empty JSON object
        response = {}
        # Return response
        return Response(response)

    def put(self, request, ruleset_pk, rule_pk, pk):
        """Update a rule tier based on its ID."""

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
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        min_value = request.data['min_value']
        max_value = request.data['max_value']
        ordinal = request.data['ordinal']
        tax_rate = request.data['tax_rate']
        # Invoke service method
        try:
            update_rule_tier(pk, min_value, max_value, ordinal, tax_rate)
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except RuleTier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Generate and return response
        response = {}
        # Return response
        return Response(response)


class SecondaryRuleTiersList(APIView):
    """Create django rest secondary rule tiers list view."""

    def post(self, request, ruleset_pk, rule_pk):
        """Create a new secondary rule tier."""

        # Define the list of required attributes
        required_attributes = [
            'primary_tier_id',
            'ordinal',
            'tax_rate'
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        primary_tier_id = request.data['primary_tier_id']
        ordinal = request.data['ordinal']
        tax_rate = request.data['tax_rate']
        # Invoke service method
        print('rule_pk = ' + str(rule_pk))
        try:
            secondary_tier_id = create_secondary_rule_tier(
                rule_pk,
                primary_tier_id,
                ordinal,
                tax_rate
            )
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except SecondaryTieredRateRule.DoesNotExist:
            return Response(
                {
                    'error': 'No rule found with id=' + str(rule_pk)
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except RuleTier.DoesNotExist:
            return Response(
                {
                    'error': 'No rule tier found with id=' +
                    str(primary_tier_id)
                },
                status=status.HTTP_404_NOT_FOUND
            )
        # Generate and return response
        response = {
            'secondary_tier_id': secondary_tier_id
        }
        # Return response
        return Response(response)


class SecondaryRuleTierDetail(APIView):
    """Create django rest secondary rule tier detail view."""

    def delete(self, request, ruleset_pk, rule_pk, pk):
        """Delete a secondary rule tier based on its ID."""

        # Call apropriate services method
        delete_secondary_rule_tier(pk)
        # Create response via empty JSON object
        response = {}
        # Return response
        return Response(response)

    def put(self, request, ruleset_pk, rule_pk, pk):
        """Update a secondary rule tier."""

        # Define the list of required attributes
        required_attributes = [
            'ordinal',
            'tax_rate'
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Extract data required for service method
        ordinal = request.data['ordinal']
        tax_rate = request.data['tax_rate']
        # Invoke service method
        try:
            update_secondary_rule_tier(pk, ordinal, tax_rate)
        except ValidationError as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except SecondaryRuleTier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except RuleTier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Generate and return response
        response = {}
        # Return response
        return Response(response)


def serialise_tax_calculation_result(result):
    """Serialise a tax calculation result to a dictionary."""
    serialised_result = {
        'calculation_id': result.id,
        'username': result.username,
        'created': result.created,
        'jurisdictions': {},
        'excluded_jurisdiction_ids': result.excluded_jurisdiction_ids,
    }

    for ruleset_result in result.results.all():
        for tier_result in ruleset_result.results.all():
            jurisdiction_id = ruleset_result.jurisdiction_id
            if jurisdiction_id not in serialised_result['jurisdictions']:
                serialised_result['jurisdictions'][jurisdiction_id] = []

            serialised_tier_result = {
                'tax_category': ruleset_result.tax_category_name,
                'ruleset_ordinal': ruleset_result.ordinal,
                'tier_ordinal': tier_result.ordinal,
                'rule_id': tier_result.rule_id,
                'rule_type': tier_result.rule_model_name,
                'tier_name': tier_result.tier_name,
                'variable_name': tier_result.variable_name,
                'variable_value': tier_result.variable_value,
                'taxable_amount': tier_result.taxable_amount,
                'tax_rate': tier_result.tax_rate,
                'tax_payable': tier_result.tax_payable,
            }

            serialised_result['jurisdictions'][jurisdiction_id].append(
                serialised_tier_result
            )

    return serialised_result


class TaxCalculationsList(APIView):
    """Create django rest tax calculation list view."""

    def post(self, request):
        """Create a new tax calculation."""

        # Define the list of required attributes
        required_attributes = [
            'username',
            'jurisdiction_ids',
            'variables',
        ]
        # Validate data
        if not contains_required_attributes(request, required_attributes):
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract required data from request
        username = request.data['username']
        jurisdiction_ids = request.data['jurisdiction_ids']
        variables = request.data['variables']

        # Invoke service method
        try:
            result = create_calculation(username, jurisdiction_ids, variables)
        except Exception as e:
            print(e)
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate response
        response = serialise_tax_calculation_result(result)

        return Response(response)

    def get(self, request):
        """Get a list of tax calculations for the specified user."""

        # Validate data
        if 'username' not in request.GET:
            return Response(
                {
                    'error': 'Invalid request. Please supply all required ' +
                    'attributes.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract data
        username = request.GET['username']

        if username is None or username == '' or username == 'None':
            return Response(
                {
                    'error': 'No tax calculations found for null or blank ' +
                    'username.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        results = get_calculations_for_user(username)

        if results.count() == 0:
            return Response(
                {
                    'error': 'No tax calculations found for user ' +
                    username + '.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        response = []
        for result in results:
            serialised_result = serialise_tax_calculation_result(result)
            response.append(serialised_result)

        return Response(response)


class TaxCalculationDetail(APIView):
    """Create django rest tax calculation detail view."""

    def get(self, request, pk):
        """Retrieve a specific tax calculation based on its ID."""

        try:
            calculation = get_calculation_by_id(pk)
        except TaxCalculationResult.DoesNotExist:
            return Response(
                {
                    'error': 'No tax calculations found for id' +
                    str(id) + '.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serialised_calculation = serialise_tax_calculation_result(calculation)
        print(str(serialised_calculation))
        return Response(serialised_calculation)
