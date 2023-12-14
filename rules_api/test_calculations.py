from .models import *
from .test_models import *
from .services import *
import pytest

# Retrieving calculations
@pytest.mark.django_db
def test_get_calculations_for_null_username():
    with pytest.raises(TaxCalculationResult.DoesNotExist):
        get_calculations_for_user(None)

@pytest.mark.django_db
def test_get_calculations_for_non_existent_username():
    with pytest.raises(TaxCalculationResult.DoesNotExist):
        get_calculations_for_user('Jimbo')

@pytest.mark.django_db
def test_get_calculations_for_valid_username():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())
    assert rule is not None

    jurisdiction_id = rule.ruleset.jurisdiction_id
    calculation = create_calculation('bob', [jurisdiction_id], create_mock_variable_table())
    assert calculation is not None
    assert calculation.results.count() == 1
    assert calculation.results.results.count() == 1

    calculations = get_calculations_for_user('bob')
    assert calculations.count() == 1
    calculation = calculations.first()
    assert calculation is not None
    assert calculation.results.count() == 1
    assert calculation.results.results.count() == 1

# Generating calculations
@pytest.mark.django_db
def test_create_calculation_with_no_jurisdictions():
    pass

@pytest.mark.django_db
def test_create_calculation_with_single_jurisdiction():
    pass

@pytest.mark.django_db
def test_create_calculation_with_multiple_jurisdictions():
    pass