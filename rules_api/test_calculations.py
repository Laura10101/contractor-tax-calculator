from .models import *
import pytest

# Retrieving calculations
@pytest.mark.django_db
def test_get_calculations_for_null_username():
    pass

@pytest.mark.django_db
def test_get_calculations_for_non_existent_username():
    pass

@pytest.mark.django_db
def test_get_calculations_for_valid_username():
    pass

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