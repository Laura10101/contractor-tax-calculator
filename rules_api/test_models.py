from .models import *
import math
import pytest

# Model tests assume that invalid models are prevented from being created
# by validation in the views and services layers.
# This validation is tested in test_services.py and test_views.py respectively.

# Helper functions
def create_empty_results_table():
    return []

def create_variable_table(primary_income, secondary_income=None):
    table = {
        'primary_income': primary_income
    }

    if secondary_income is not None:
        table['secondary_income'] = secondary_income
    
    return table

# Test flat rate calculations
def test_flat_rate_calculate():
    primary_income = 70000
    flat_rate = 10
    rule = FlatRateRule(
        variable_name='primary_income',
        flat_rate = flat_rate
    )
    variables = create_variable_table(primary_income)
    results = create_empty_results_table()
    rule.calculate(variables, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == primary_income * (flat_rate / 100)


# Test rule tier calculations
def test_rule_tier_calculate_where_income_below_boundary():
    primary_income = 9999
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    results = create_empty_results_table()
    tier.calculate(primary_income, results)
    assert len(results) == 0

def test_rule_tier_calculate_where_income_on_lower_boundary():
    primary_income = 10000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    results = create_empty_results_table()
    tier.calculate(primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round((primary_income - tier.min_value) * (tier.tier_rate / 100), 2)

def test_rule_tier_calculate_where_income_within_boundaries():
    primary_income = 25000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    results = create_empty_results_table()
    tier.calculate(primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round((primary_income - tier.min_value) * (tier.tier_rate / 100), 2)

def test_rule_tier_calculate_where_income_on_upper_boundary():
    primary_income = 45000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    results = create_empty_results_table()
    tier.calculate(primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round((tier.max_value - tier.min_value) * (tier.tier_rate / 100), 2)

def test_rule_tier_calculate_where_income_above_upper_boundary():
    primary_income = 45001
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    results = create_empty_results_table()
    tier.calculate(primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round((tier.max_value - tier.min_value) * (tier.tier_rate / 100), 2)

def test_rule_tier_calculate_where_no_upper_boundary_and_income_above_lower_boundary():
    primary_income = 45001
    tier = RuleTier(min_value=10000, tier_rate=10)
    results = create_empty_results_table()
    tier.calculate(primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round((primary_income - tier.min_value) * (tier.tier_rate / 100), 2)

# Test secondary rule tier calculations
def test_secondary_tier_calculate_where_total_income_below_lower_boundary():
    primary_income = 9999
    secondary_income = 0
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)
    assert len(results) == 0

def test_secondary_tier_calculate_where_primary_income_on_lower_boundary_and_no_secondary_income():
    primary_income = 10000
    secondary_income = 0
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)
    assert len(results) == 0

def test_secondary_tier_calculate_where_primary_income_on_lower_boundary_and_total_within_boundaries():
    primary_income = 10000
    secondary_income = 10000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round(secondary_income * (tier.tier_rate / 100), 2)

def test_secondary_tier_calculate_where_primary_income_and_total_within_boundaries():
    primary_income = 20000
    secondary_income = 10000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)
    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round(secondary_income * (tier.tier_rate / 100), 2)

def test_secondary_tier_calculate_where_primary_income_within_boundaries_and_total_exceeds():
    primary_income = 35000
    secondary_income = 20000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)

    tier_amount = tier.max_value - tier.min_value
    tier_amount_remaining = tier_amount - (primary_income - tier.min_value)

    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round(tier_amount_remaining * (tier.tier_rate / 100), 2)

def test_secondary_tier_calculate_where_primary_income_on_upper_boundary_and_total_exceeds():
    primary_income = 45000
    secondary_income = 20000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)

    tier_amount = tier.max_value - tier.min_value
    tier_amount_remaining = tier_amount - (primary_income - tier.min_value)

    assert len(results) == 1
    assert results[0] is not None
    assert results[0]['tax_subtotal'] == round(tier_amount_remaining * (tier.tier_rate / 100), 2)

def test_secondary_tier_calculate_where_primary_income_above_upper_boundary():
    primary_income = 45001
    secondary_income = 20000
    tier = RuleTier(min_value=10000, max_value=45000, tier_rate=10)
    secondary_tier = SecondaryRuleTier(primary_tier=tier, tier_rate=10)
    results = create_empty_results_table()
    secondary_tier.calculate(secondary_income, primary_income, results)

    tier_amount = tier.max_value - tier.min_value
    tier_amount_remaining = tier_amount - (primary_income - tier.min_value)
    assert len(results) == 0

# Test iteration over rule tiers
def test_tiered_rule_iteration_with_no_tiers_defined():
    rule = TieredRateRule()
    rule.reset()
    assert rule.next() is None

def test_tiered_rule_iteration_with_single_tier_defined():
    tier = RuleTier(min_value=0, max_value=100)
    rule = TieredRateRule(first_tier=tier)
    assert rule.next() is None
    rule.reset()
    next_tier = rule.next()
    assert next_tier is not None
    assert next_tier.min_value == 0
    assert next_tier.max_value == 100
    next_tier = rule.next()
    assert next_tier is None

def test_tiered_rule_iteration_with_multiple_tiers_defined():
    tier2 = RuleTier(min_value=101, max_value=200)
    tier1 = RuleTier(min_value=0, max_value=100, next=tier2)
    rule = TieredRateRule(first_tier=tier1)
    assert rule.next() is None
    rule.reset()
    next_tier = rule.next()
    assert next_tier is not None
    assert next_tier.min_value == 0
    assert next_tier.max_value == 100
    next_tier = rule.next()
    assert next_tier is not None
    assert next_tier.min_value == 101
    assert next_tier.max_value == 200
    next_tier = rule.next()
    assert next_tier is None

# Test iteration over secondary rule tiers
def test_secondary_tiered_rule_iteration_with_no_tiers_defined():
    rule = SecondaryTieredRateRule()
    rule.reset()
    assert rule.next() is None

def test_secondary_tiered_rule_iteration_with_single_tier_defined():
    ptier1 = RuleTier(min_value=0, max_value=100)

    tier1 = SecondaryRuleTier(primary_tier=ptier1)
    rule = SecondaryTieredRateRule(first_tier=tier1)
    assert rule.next() is None
    rule.reset()
    next_tier = rule.next()
    assert next_tier is not None
    assert next_tier.primary_rule.min_value == 0
    assert next_tier.primary_rule.max_value == 100
    next_tier = rule.next()
    assert next_tier is None

def test_secondary_tiered_rule_iteration_with_multiple_tiers_defined():
    ptier2 = RuleTier(min_value=101, max_value=200)
    ptier1 = RuleTier(min_value=0, max_value=100, next=tier2)

    tier2 = SecondaryRuleTier(primary_tier=ptier1)
    tier1 = SecondaryRuleTier(primary_tier=ptier1, next=tier2)
    rule = SecondaryTieredRateRule(first_tier=tier1)
    assert rule.next() is None
    rule.reset()
    next_tier = rule.next()
    assert next_tier is not None
    assert next_tier.primary_rule.min_value == 0
    assert next_tier.primary_rule.max_value == 100
    next_tier = rule.next()
    assert next_tier is not None
    assert next_tier.primary_rule.min_value == 101
    assert next_tier.primary_rule.max_value == 200
    next_tier = rule.next()
    assert next_tier is None

# Test iteration over rules within a ruleset
def test_ruleset_iteration_with_no_rules_defined():
    rs = RuleSet()
    assert rs.next() is None
    rs.reset()
    assert rs.next() is None

def test_ruleset_iteration_with_single_rule_defined():
    rule1 = FlatRateRule(name='A')
    rs = RuleSet(first_rule=rule1)
    assert rs.next() is None
    rs.reset()
    next_rule = rs.next()
    assert next_rule.name == 'A'
    assert rs.next() is None

def test_ruleset_iteration_with_multiple_rules_defined():
    rule2 = FlatRateRule(name='B')
    rule1 = FlatRateRule(name='A', next=rule2)
    rs = RuleSet(first_rule=rule1)
    assert rs.next() is None
    rs.reset()
    next_rule = rs.next()
    assert next_rule.name == 'A'
    next_rule = rs.next()
    assert next_rule.name == 'B'
    assert rs.next() is None

