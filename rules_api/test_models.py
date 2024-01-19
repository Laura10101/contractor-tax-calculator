from .models import *
import pytest

from jurisdictions_api.models import Jurisdiction

# Model tests assume that invalid models are prevented from being created
# by validation in the views and services layers.
# This validation is tested in test_services.py and test_views.py respectively.

# Helper functions
def create_mock_jurisdiction():
    jurisdiction_count = Jurisdiction.objects.count()
    return Jurisdiction.objects.create(name='Test Jurisdiction ' + str(jurisdiction_count))

def create_mock_tax_calculation_result(username='bob'):
    return TaxCalculationResult.objects.create(username=username)

def create_mock_ruleset_calculation_result():
    tax_calculation_result = create_mock_tax_calculation_result()
    return TaxRuleSetResult.objects.create(
        tax_calculation_result=tax_calculation_result,
        jurisdiction_id=1,
        tax_category_id=1,
        tax_category_name='Test',
        ordinal=1
    )

def create_mock_variable_table(salary=9000, dividends=50000, company_profit=100000):
    return {
        'salary': salary,
        'dividends': dividends,
        'company_profit': company_profit
    }

def create_mock_ruleset():
    jurisdiction_count = Jurisdiction.objects.count()
    jurisdiction = Jurisdiction.objects.create(name='Test Jurisdiction ' + str(jurisdiction_count))
    tax_category = TaxCategory.objects.create(name='Test Category ' + str(TaxCategory.objects.count()))
    ruleset = RuleSet.objects.create(
        jurisdiction_id=jurisdiction.id,
        tax_category=tax_category,
        ordinal=1
    )
    return ruleset

def create_mock_flat_rate_Rule(variable_name, rate, ruleset=None):
    if ruleset is None:
        ruleset = create_mock_ruleset()

    return FlatRateRule.objects.create(
        ruleset=ruleset,
        variable_name=variable_name,
        name='Rule Test',
        ordinal=1,
        flat_rate=rate
    )

def create_mock_tiered_rate_rule(variable_name, ordinal=1, ruleset=None):
    if ruleset is None:
        ruleset = create_mock_ruleset()
    rule = TieredRateRule.objects.create(
        variable_name=variable_name,
        ruleset=ruleset,
        name='Rule Test',
        ordinal=ordinal
    )
    return rule

def create_mock_rule_tier(rule, min_value, max_value, tax_rate):
    rule_tier = RuleTier.objects.create(
        rule=rule,
        min_value=min_value,
        max_value=max_value,
        ordinal=1,
        tier_rate=tax_rate
    )
    return rule_tier

def create_mock_simple_tiered_rate_rule(min_value, max_value, variable_name, tax_rate):
    rule = create_mock_tiered_rate_rule(variable_name)
    rule_tier = create_mock_rule_tier(rule, min_value, max_value, tax_rate)
    return rule

def create_mock_secondary_tiered_rate_rule(primary_rule, variable_name, ruleset=None):
    if ruleset is None:
        ruleset = primary_rule.ruleset
    return SecondaryTieredRateRule.objects.create(
        primary_rule=primary_rule,
        ruleset=ruleset,
        name='Secondary Tiered Rule Test',
        ordinal=1,
        variable_name=variable_name
    )

def create_mock_secondary_rule_tier(secondary_rule, primary_tier, tier_rate):
    return SecondaryRuleTier.objects.create(secondary_rule=secondary_rule, primary_tier=primary_tier, ordinal=1, tier_rate=tier_rate)

def create_mock_simple_secondary_tiered_rate_rule(min_value, max_value, primary_variable,
            secondary_variable, primary_rate, secondary_rate):
    primary_rule = create_mock_tiered_rate_rule(primary_variable)
    primary_tier = create_mock_rule_tier(primary_rule, min_value, max_value, primary_rate)

    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, secondary_variable)
    secondary_tier = create_mock_secondary_rule_tier(secondary_rule, primary_tier, secondary_rate)
    return secondary_rule


# Test flat rate calculations
@pytest.mark.django_db
def test_flat_rate_calculate():
    flat_rate = 20
    rule = FlatRateRule.objects.create(
        variable_name='company_profit',
        flat_rate = flat_rate,
        ruleset=create_mock_ruleset(),
        name='Flat Rate Test',
        ordinal=1
    )
    variables = create_mock_variable_table()
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == variables['company_profit'] * (flat_rate / 100)


# Test rule tier calculations
@pytest.mark.django_db
def test_rule_tier_calculate_where_income_below_boundary():
    rule = create_mock_simple_tiered_rate_rule(10000, 45000, 'salary', 20)
    variables = create_mock_variable_table()
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 0

@pytest.mark.django_db
def test_rule_tier_calculate_where_income_on_lower_boundary():
    rule = create_mock_simple_tiered_rate_rule(9000, 45000, 'salary', 20)
    variables = create_mock_variable_table()
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((variables['salary'] - 9000) * (20 / 100), 2)

@pytest.mark.django_db
def test_rule_tier_calculate_where_income_within_boundaries():
    rule = create_mock_simple_tiered_rate_rule(9000, 45000, 'salary', 20)
    variables = create_mock_variable_table(salary=25000)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((25000 - 9000) * (20 / 100), 2)

@pytest.mark.django_db
def test_rule_tier_calculate_where_income_on_upper_boundary():
    rule = create_mock_simple_tiered_rate_rule(9000, 45000, 'salary', 20)
    variables = create_mock_variable_table(salary=45000)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((45000 - 9000) * (20 / 100), 2)

@pytest.mark.django_db
def test_rule_tier_calculate_where_income_above_upper_boundary():
    rule = create_mock_simple_tiered_rate_rule(9000, 45000, 'salary', 20)
    variables = create_mock_variable_table(salary=45001)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((45000 - 9000) * (20 / 100), 2)

@pytest.mark.django_db
def test_rule_tier_calculate_where_no_upper_boundary_and_income_above_lower_boundary():
    rule = create_mock_simple_tiered_rate_rule(9000, None, 'salary', 20)
    variables = create_mock_variable_table(salary=45000)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((45000 - 9000) * (20 / 100), 2)

# Test secondary rule tier calculations
@pytest.mark.django_db
def test_secondary_tier_calculate_where_total_income_below_lower_boundary():
    rule = create_mock_simple_secondary_tiered_rate_rule(1000000, 4000000, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table()
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 0

@pytest.mark.django_db
def test_secondary_tier_calculate_where_primary_income_on_lower_boundary_and_no_secondary_income():
    primary_income = 10000
    secondary_income = 0
    tier_min = primary_income
    tier_max = 45000
    rule = create_mock_simple_secondary_tiered_rate_rule(tier_min, tier_max, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table(salary=primary_income, dividends=secondary_income)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 0

@pytest.mark.django_db
def test_secondary_tier_calculate_where_primary_income_on_lower_boundary_and_total_within_boundaries():
    primary_income = 10000
    secondary_income = 10000
    tier_min = 10000
    tier_max = 45000
    rule = create_mock_simple_secondary_tiered_rate_rule(tier_min, tier_max, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table(salary=primary_income, dividends=secondary_income)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round(secondary_income * (8 / 100), 2)

@pytest.mark.django_db
def test_secondary_tier_calculate_where_primary_income_and_total_within_boundaries():
    primary_income = 20000
    secondary_income = 10000
    tier_min = 10000
    tier_max = 45000
    rule = create_mock_simple_secondary_tiered_rate_rule(tier_min, tier_max, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table(salary=primary_income, dividends=secondary_income)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round(secondary_income * (8 / 100), 2)

@pytest.mark.django_db
def test_secondary_tier_calculate_where_primary_income_within_boundaries_and_total_exceeds():
    primary_income = 35000
    secondary_income = 20000
    tier_min = 10000
    tier_max = 45000
    tier_amount = tier_max - tier_min
    tier_amount_remaining = tier_amount - (primary_income - tier_min)

    rule = create_mock_simple_secondary_tiered_rate_rule(tier_min, tier_max, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table(salary=primary_income, dividends=secondary_income)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round(tier_amount_remaining * (8 / 100), 2)

@pytest.mark.django_db
def test_secondary_tier_calculate_where_primary_income_on_upper_boundary_and_total_exceeds():
    primary_income = 45000
    secondary_income = 20000
    tier_min = 10000
    tier_max = 45000
    rule = create_mock_simple_secondary_tiered_rate_rule(tier_min, tier_max, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table(salary=primary_income, dividends=secondary_income)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 0

@pytest.mark.django_db
def test_secondary_tier_calculate_where_primary_income_above_upper_boundary():
    primary_income = 45001
    secondary_income = 20000
    tier_min = 10000
    tier_max = 45000
    rule = create_mock_simple_secondary_tiered_rate_rule(tier_min, tier_max, 'salary', 'dividends', 20, 8)
    variables = create_mock_variable_table(salary=primary_income, dividends=secondary_income)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 0

# Test iteration over rule tiers
@pytest.mark.django_db
def test_tiered_rule_iteration_with_no_tiers_defined():
    rule = create_mock_tiered_rate_rule('salary')
    variables = create_mock_variable_table()
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 0

@pytest.mark.django_db
def test_tiered_rule_iteration_with_single_tier_defined():
    rule = create_mock_simple_tiered_rate_rule(9000, 45000, 'salary', 20)
    variables = create_mock_variable_table(salary=25000)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((25000 - 9000) * (20 / 100), 2)

@pytest.mark.django_db
def test_tiered_rule_iteration_with_multiple_tiers_defined():
    rule = create_mock_simple_tiered_rate_rule(9000, 45000, 'salary', 20)
    second_tier = create_mock_rule_tier(rule, 45001, 100000, 45)
    variables = create_mock_variable_table(salary=75000)
    results = create_mock_ruleset_calculation_result()
    rule.calculate(variables, results)
    assert len(results.results.values()) == 2

    # Calculate the amount of tax payable under the first tier 20% rate
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == round((45000 - 9000) * (20 / 100), 2)

    # Calculate the amount of tax payable under the second tier 45% rate
    assert results.results.values()[1] is not None
    assert results.results.values()[1]['tax_payable'] == round((75000 - 45001) * (45 / 100), 2)

# Test iteration over secondary rule tiers
@pytest.mark.django_db
def test_secondary_tiered_rule_iteration_with_no_tiers_defined():
    ruleset = create_mock_ruleset()
    primary_rule = create_mock_tiered_rate_rule('salary', 1, ruleset)
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends')
    variables = create_mock_variable_table()
    results = create_mock_ruleset_calculation_result()
    secondary_rule.calculate(variables, results)
    assert len(results.results.values()) == 0

@pytest.mark.django_db
def test_secondary_tiered_rule_iteration_with_single_tier_defined():
    secondary_rate_rule = create_mock_simple_secondary_tiered_rate_rule(10000, 45000, 'salary', 'dividends', 20, 8)

    variables = create_mock_variable_table(salary=9000, dividends=50000)
    results = create_mock_ruleset_calculation_result()
    secondary_rate_rule.calculate(variables, results)
    
    # None of this tier has been used by the primary income
    # Calculate tier remaining for use by secondary income as max - min
    tier_remaining = 45000 - 10000
    # Dividends is 50000 so all of this tier will be used up
    # Taxable amount is therefore just the tier remaining
    taxable_amount = tier_remaining
    tax_payable = round(taxable_amount * (8/100), 2)

    assert len(results.results.values()) == 1
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == tax_payable

@pytest.mark.django_db
def test_secondary_tiered_rule_iteration_with_multiple_tiers_defined():
    secondary_rate_rule = create_mock_simple_secondary_tiered_rate_rule(10000, 45000, 'salary', 'dividends', 20, 8)

    second_primary_tier = create_mock_rule_tier(secondary_rate_rule.primary_rule, 45001, 100000, 45)
    second_secondary_tier = create_mock_secondary_rule_tier(secondary_rate_rule, second_primary_tier, 40)

    variables = create_mock_variable_table(salary=9000, dividends=50000)
    results = create_mock_ruleset_calculation_result()
    secondary_rate_rule.calculate(variables, results)
    
    # None of this tier has been used by the primary income
    # Calculate tier remaining for use by secondary income as max - min
    tier_remaining = 45000 - 10000
    # Dividends is 50000 so all of this tier will be used up
    # Taxable amount is therefore just the tier remaining
    taxable_amount = tier_remaining
    tax_payable = round(taxable_amount * (8/100), 2)

    assert len(results.results.values()) == 2
    assert results.results.values()[0] is not None
    assert results.results.values()[0]['tax_payable'] == tax_payable

    # Similarly none of the second secondary tier has been used by primary income
    # However, dividends is not enough to use all of this up
    tier_remaining = 100000 - 45001
    dividends_remaining = variables['dividends'] - (45001 - variables['salary'])
    taxable_amount = dividends_remaining
    tax_payable = round(taxable_amount * (40/100), 2)

    assert results.results.values()[1] is not None
    assert results.results.values()[1]['tax_payable'] == tax_payable

# Test iteration over rules within a ruleset/
@pytest.mark.django_db
def test_ruleset_iteration_with_no_rules_defined():
    ruleset = create_mock_ruleset()
    variables = create_mock_variable_table(salary=75000)
    results = create_mock_tax_calculation_result()
    ruleset.calculate(variables, results)
    assert len(results.results.values()) == 0


@pytest.mark.django_db
def test_ruleset_iteration_with_single_rule_defined():
    ruleset = create_mock_ruleset()
    variables = create_mock_variable_table()
    results = create_mock_tax_calculation_result()

    dividend_rule = create_mock_flat_rate_Rule('dividends', 8, ruleset)
    ruleset.calculate(variables, results)
    assert len(results.results.values()) == 1

    ruleset_result = results.results.first()

    assert len(ruleset_result.results.values()) == 1
    assert ruleset_result.results.values()[0] is not None
    assert ruleset_result.results.values()[0]['tax_payable'] == round(variables['dividends'] * (8 / 100), 2)


@pytest.mark.django_db
def test_ruleset_iteration_with_multiple_rules_defined():
    ruleset = create_mock_ruleset()
    variables = create_mock_variable_table(salary=30000)
    results = create_mock_tax_calculation_result()

    dividend_rule = create_mock_flat_rate_Rule('dividends', 8, ruleset)
    print(ruleset.rules.count())

    salary_rule = create_mock_tiered_rate_rule('salary', 2, ruleset)
    print(ruleset.rules.count())

    tier1 = create_mock_rule_tier(salary_rule, 10000, 45000, 20)
    assert ruleset.rules.count() == 2

    ruleset.calculate(variables, results)

    valid_results = [
        round(variables['dividends'] * (8 / 100), 2),
        round((variables['salary'] - 10000) * (20/100), 2)
    ]
    ruleset_result = results.results.first()

    for tier_result in ruleset_result.results.all():
        print(tier_result)
        assert tier_result is not None
        assert tier_result.tax_payable in valid_results
    
    assert ruleset_result.results.count() == 2
    
