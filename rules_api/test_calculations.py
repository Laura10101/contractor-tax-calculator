from .models import *
from .test_models import *
from .services import *
from django.core.exceptions import ValidationError
import pytest

# Retrieving calculations


@pytest.mark.django_db
def test_get_calculations_for_null_username():
    calculations = get_calculations_for_user(None)
    assert calculations.count() == 0


@pytest.mark.django_db
def test_get_calculations_for_non_existent_username():
    calculations = get_calculations_for_user('Jimbo')
    assert calculations.count() == 0


@pytest.mark.django_db
def test_get_calculations_for_valid_username():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())
    assert rule is not None

    jurisdiction_id = rule.ruleset.jurisdiction_id
    calculation = create_calculation(
        'bob',
        [jurisdiction_id],
        create_mock_variable_table()
    )
    assert calculation is not None
    assert calculation.results.count() == 1
    assert calculation.results.first().results.count() == 1

    calculations = get_calculations_for_user('bob')
    assert calculations.count() == 1
    calculation = calculations.first()
    assert calculation is not None
    assert calculation.results.count() == 1
    assert calculation.results.first().results.count() == 1

# Generating calculations


@pytest.mark.django_db
def test_create_calculation_with_no_jurisdictions():
    with pytest.raises(ValidationError):
        create_calculation('bob', [], create_mock_variable_table)


@pytest.mark.django_db
def test_create_calculation_with_single_jurisdiction():
    rule = create_mock_simple_tiered_rate_rule(8000, 45000, 'salary', 20)
    jursdiction_id = rule.ruleset.jurisdiction_id
    variable_table = create_mock_variable_table()
    calculation = create_calculation('bob', [jursdiction_id], variable_table)

    assert calculation is not None
    assert calculation.results.count() == 1
    assert calculation.results.first().results.count() == 1

    ruleset_result = calculation.results.first()
    tier_result = ruleset_result.results.first()

    assert tier_result.tax_payable == round(1000 * (20/100), 2)


@pytest.mark.django_db
def test_create_calculation_with_multiple_single_rule_jurisdictions():
    rule1 = create_mock_simple_tiered_rate_rule(8000, 45000, 'salary', 20)
    jursdiction_id_1 = rule1.ruleset.jurisdiction_id

    rule2 = create_mock_flat_rate_Rule('dividends', 8, create_mock_ruleset())
    jursdiction_id_2 = rule2.ruleset.jurisdiction_id

    variable_table = create_mock_variable_table()
    calculation = create_calculation(
        'bob',
        [jursdiction_id_1, jursdiction_id_2],
        variable_table
    )

    assert calculation is not None
    assert calculation.results.count() == 2
    ruleset_result_1 = calculation.results.first()
    assert ruleset_result_1.results.count() == 1
    assert ruleset_result_1.results.first().tax_payable == round(1000 * 0.2, 2)

    ruleset_result_2 = calculation.results.all()[1]
    assert ruleset_result_2.results.count() == 1
    expected_tax = round(variable_table['dividends'] * (8/100), 2)
    assert ruleset_result_2.results.first().tax_payable == expected_tax
