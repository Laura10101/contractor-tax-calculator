from .models import *
from .services import *
from .views import *
from .test_models import *
import pytest
from rest_framework.test import APIClient

client = APIClient()
url = '/api/rules/'

# Ruleset creation
@pytest.mark.django_db
def test_post_ruleset_with_null_data():
    jurisdiction_id = None
    tax_category_id = None

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 400

@pytest.mark.django_db
def test_post_ruleset_with_null_jurisdiction_id():
    jurisdiction_id = None
    tax_category_id = create_tax_category('Test category')

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 400

@pytest.mark.django_db
def test_post_ruleset_with_null_tax_category_id():
    jurisdiction_id = create_mock_jurisdiction()
    tax_category_id = None

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 400

@pytest.mark.django_db
def test_post_ruleset_with_non_existent_tax_category_id():
    jurisdiction_id = create_mock_jurisdiction()
    tax_category_id = 479

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 400

@pytest.mark.django_db
def test_post_ruleset_with_duplicate_tax_category_jurisdiction_combination():
    jurisdiction_id = create_mock_jurisdiction()
    tax_category_id = create_tax_category('Test category')

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 200
    assert response.data['tax_category_id'] is not None

    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 409

@pytest.mark.django_db
def test_post_valid_ruleset():
    jurisdiction_id = create_mock_jurisdiction()
    tax_category_id = create_tax_category('Test category')

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 200
    assert response.data['tax_category_id'] is not None

# Ruleset deletion
@pytest.mark.django_db
def test_delete_ruleset_with_null_id():
    ruleset_id = None

    request_url = url + 'rulesets/' + str(ruleset_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status == 404

@pytest.mark.django_db
def test_delete_ruleset_with_non_existent_id():
    ruleset_id = 479

    request_url = url + 'rulesets/' + str(ruleset_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status == 404

@pytest.mark.django_db
def test_delete_ruleset():
    ruleset_id = create_mock_ruleset().id

    request_url = url + 'rulesets/' + str(ruleset_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status == 200

# Tax category creation
@pytest.mark.django_db
def test_post_tax_category_with_null_name():
    name = None

    body = {
        'name': name,
    }

    request_url = url + 'taxcategories/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 400

@pytest.mark.django_db
def test_post_tax_category_with_duplicate_name():
    name = 'Test category'

    id = create_tax_category(name)
    assert id is not None

    body = {
        'name': name,
    }

    request_url = url + 'taxcategories/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 409

@pytest.mark.django_db
def test_post_valid_tax_category():
    name = 'Test category'

    body = {
        'name': name,
    }

    request_url = url + 'taxcategories/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status == 200
    assert response.data['tax_category_id'] is not None

#  Tax category deletion
@pytest.mark.django_db
def test_delete_tax_category_with_null_id():
    id = None

    request_url = url + 'taxcategories/' + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status == 404

@pytest.mark.django_db
def test_delete_tax_category_with_non_existent_id():
    id = 479

    request_url = url + 'taxcategories/' + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status == 404

@pytest.mark.django_db
def test_delete_tax_category():
    id = create_tax_category('Test category')

    request_url = url + 'taxcategories/' + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status == 200

# Rule deletion
@pytest.mark.django_db
def test_delete_rule_with_null_id():
    pass

@pytest.mark.django_db
def test_delete_rule_with_non_existent_id():
    pass

@pytest.mark.django_db
def test_delete_rule():
    pass

# Flat rate rule creation
@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_data():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_existent_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_numeric_ruleset_id():
    pass

@pytest.mark.django_db
def test_crete_flat_rate_rule_with_null_name():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_nulL_explainer():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_variable_name():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_flat_rate():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_numeric_flat_rate():
    pass

@pytest.mark.django_db
def test_post_flat_rate_rule_with_negative_flat_rate():
    pass

@pytest.mark.django_db
def test_post_valid_flat_rate_rule():
    pass

# Flat rate rule updates
@pytest.mark.django_db
def test_patch_flat_rate_rule_with_null_data():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_null_rule_id():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_non_existent_rule_id():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_non_numeric_rule_id():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_null_name():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_nulL_explainer():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_null_variable_name():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_null_flat_rate():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_non_numeric_flat_rate():
    pass

@pytest.mark.django_db
def test_patch_flat_rate_rule_with_negative_flat_rate():
    pass

@pytest.mark.django_db
def test_patch_valid_flat_rate_rule():
    pass


# Tiered rate rule creation
@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_data():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_non_existent_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_non_numeric_ruleset_id():
    pass

@pytest.mark.django_db
def test_crete_tiered_rate_rule_with_null_name():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_nulL_explainer():
    pass

@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_variable_name():
    pass

@pytest.mark.django_db
def test_post_valid_tiered_rate_rule():
    pass

# Tiered rate rule updates
@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_null_data():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_null_rule_id():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_non_existent_rule_id():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_non_numeric_rule_id():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_null_name():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_nulL_explainer():
    pass

@pytest.mark.django_db
def test_patch_tiered_rate_rule_with_null_variable_name():
    pass

@pytest.mark.django_db
def test_patch_valid_tiered_rate_rule():
    pass

# Rule tier creation
@pytest.mark.django_db
def test_post_rule_tier_with_null_data():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_null_rule_id():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_non_existent_rule_id():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_rule_id():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_null_min_value():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_min_value():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_null_max_value():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_max_value():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_null_tier_rate():
    pass

@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_tier_rate():
    pass

@pytest.mark.django_db
def test_post_valid_rule_tier():
    pass

# Rule tier updates
@pytest.mark.django_db
def test_patch_rule_tier_with_null_data():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_null_tier_id():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_non_existent_tier_id():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_non_numeric_tier_id():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_null_min_value():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_non_numeric_min_value():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_null_max_value():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_non_numeric_max_value():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_null_tier_rate():
    pass

@pytest.mark.django_db
def test_patch_rule_tier_with_non_numeric_tier_rate():
    pass

@pytest.mark.django_db
def test_patch_valid_rule_tier():
    pass

# Secondary tiered rate rule creation
@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_data():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_existent_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_numeric_ruleset_id():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_primary_rule_id():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_existent_primary_rule_id():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_numeric_primary_rule_id():
    pass

@pytest.mark.django_db
def test_crete_secondary_iered_rate_rule_with_null_name():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_nulL_explainer():
    pass

@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_variable_name():
    pass

@pytest.mark.django_db
def test_post_valid_secondary_tiered_rate_rule():
    pass

# Secondary tiered rate rule updates
@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_null_data():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_null_rule_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_non_existent_rule_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_non_numeric_rule_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_iered_rate_rule_with_null_name():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_null_ordinal():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_non_numeric_ordinal():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_nulL_explainer():
    pass

@pytest.mark.django_db
def test_patch_secondary_tiered_rate_rule_with_null_variable_name():
    pass

@pytest.mark.django_db
def test_patch_valid_secondary_tiered_rate_rule():
    pass

# Secondary rule tier creation
@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_data():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_rule_id():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_existent_rule_id():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_rule_id():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_primary_tier_id():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_existent_primary_tier_id():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_primary_tier_id():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_tier_rate():
    pass

@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_tier_rate():
    pass

@pytest.mark.django_db
def test_post_valid_secondary_rule_tier():
    pass

# Secondary rule tier updates
@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_null_data():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_null_tier_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_non_existent_tier_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_non_numeric_tier_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_null_primary_tier_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_non_existent_primary_tier_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_non_numeric_primary_tier_id():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_null_tier_rate():
    pass

@pytest.mark.django_db
def test_patch_secondary_rule_tier_with_non_numeric_tier_rate():
    pass

@pytest.mark.django_db
def test_patch_valid_secondary_rule_tier():
    pass
