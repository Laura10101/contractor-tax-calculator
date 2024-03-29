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
    ordinal = None

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_ruleset_with_null_jurisdiction_id():
    jurisdiction_id = None
    tax_category_id = create_tax_category('Test category')
    ordinal = 1

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_ruleset_with_null_tax_category_id():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = None
    ordinal = 1

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_ruleset_with_non_existent_tax_category_id():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = 479
    ordinal = 1

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_ruleset_with_null_ordinal():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = create_tax_category('Test category')
    ordinal = None

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_ruleset_with_non_numeric_ordinal():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = create_tax_category('Test category')
    ordinal = 'ABC'

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_ruleset_with_duplicate_tax_category_jurisdiction_combination():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = create_tax_category('Test category')
    ordinal = 1

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['ruleset_id'] is not None

    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 409


@pytest.mark.django_db
def test_post_valid_ruleset():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = create_tax_category('Test category')
    ordinal = 1

    body = {
        'jurisdiction_id': jurisdiction_id,
        'tax_category_id': tax_category_id,
        'ordinal': ordinal,
    }

    request_url = url + 'rulesets/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['ruleset_id'] is not None


# Ruleset deletion


@pytest.mark.django_db
def test_delete_ruleset_with_null_id():
    ruleset_id = None

    request_url = url + 'rulesets/' + str(ruleset_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_ruleset_with_non_existent_id():
    ruleset_id = 479

    request_url = url + 'rulesets/' + str(ruleset_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_ruleset():
    ruleset_id = create_mock_ruleset().id

    request_url = url + 'rulesets/' + str(ruleset_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 200

    with pytest.raises(RuleSet.DoesNotExist):
        RuleSet.objects.get(pk=ruleset_id)


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
    assert response.status_code == 400


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
    assert response.status_code == 409


@pytest.mark.django_db
def test_post_valid_tax_category():
    name = 'Test category'

    body = {
        'name': name,
    }

    request_url = url + 'taxcategories/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['tax_category_id'] is not None


#  Tax category deletion


@pytest.mark.django_db
def test_delete_tax_category_with_null_id():
    id = None

    request_url = url + 'taxcategories/' + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_tax_category_with_non_existent_id():
    id = 479

    request_url = url + 'taxcategories/' + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_tax_category():
    id = create_tax_category('Test category')

    request_url = url + 'taxcategories/' + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 200

    with pytest.raises(TaxCategory.DoesNotExist):
        TaxCategory.objects.get(pk=id)


# Rule deletion


@pytest.mark.django_db
def test_delete_rule_with_null_id():
    id = None

    request_url = url + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_rule_with_non_existent_id():
    id = 479

    request_url = url + str(id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_rule():
    rule = create_mock_flat_rate_Rule('salary', 10, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id) + '/'
    response = client.delete(request_url, format='json')

    assert response is not None
    assert response.status_code == 200


# Flat rate rule creation


@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_data():
    ruleset_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None
    flat_rate = None

    body = {
        'ruleset_id': ruleset_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'flat_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_ruleset_id():
    ruleset_id = None
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'ruleset_id': ruleset_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'flat_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_existent_ruleset_id():
    ruleset_id = 479
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_numeric_ruleset_id():
    ruleset_id = 'ABC'
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_crete_flat_rate_rule_with_null_name():
    ruleset_id = create_mock_ruleset().id
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_ordinal():
    ruleset_id = create_mock_ruleset().id
    print(ruleset_id)
    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_numeric_ordinal():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_flat_rate_rule_with_nulL_explainer():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['rule_id'] is not None

    rule_id = response.data['rule_id']
    rule = FlatRateRule.objects.get(pk=rule_id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate


@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_variable_name():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_flat_rate_rule_with_null_flat_rate():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = None

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_flat_rate_rule_with_non_numeric_flat_rate():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 'ABC'

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_flat_rate_rule_with_negative_flat_rate():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = -20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_valid_flat_rate_rule():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['rule_id'] is not None

    rule_id = response.data['rule_id']
    rule = FlatRateRule.objects.get(pk=rule_id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate


# Flat rate rule updates


@pytest.mark.django_db
def test_put_flat_rate_rule_with_null_data():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = None
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': None,
        'ordinal': None,
        'explainer': None,
        'variable_name': None,
        'tax_rate': None,
    }

    request_url = url + 'rulesets/' + str(None) + '/rules/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_flat_rate_rule_with_null_rule_id():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = None
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_flat_rate_rule_with_non_existent_rule_id():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = 479
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_flat_rate_rule_with_non_numeric_rule_id():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = 'ABC'
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_flat_rate_rule_with_null_name():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = None
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_flat_rate_rule_with_null_ordinal():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = None
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_flat_rate_rule_with_non_numeric_ordinal():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 'ABC'
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_flat_rate_rule_with_nulL_explainer():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 2
    explainer = None
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    rule = FlatRateRule.objects.get(pk=rule_id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate


@pytest.mark.django_db
def test_put_flat_rate_rule_with_null_variable_name():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = None
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_flat_rate_rule_with_null_flat_rate():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = None

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_flat_rate_rule_with_non_numeric_flat_rate():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 'ABC'

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_flat_rate_rule_with_negative_flat_rate():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = -30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_valid_flat_rate_rule():
    rule = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = rule.id
    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'
    flat_rate = 30

    body = {
        'type': 'flat_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
        'tax_rate': flat_rate,
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    rule = FlatRateRule.objects.get(pk=rule_id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate


# Tiered rate rule creation


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_data():
    ruleset_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_ruleset_id():
    ruleset_id = None
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_non_existent_ruleset_id():
    ruleset_id = 479
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_non_numeric_ruleset_id():
    ruleset_id = 'ABC'
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_tiered_rate_rule_with_null_name():
    ruleset_id = create_mock_ruleset().id
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_ordinal():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_non_numeric_ordinal():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_nulL_explainer():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['rule_id'] is not None

    rule_id = response.data['rule_id']
    rule = TieredRateRule.objects.get(pk=rule_id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


@pytest.mark.django_db
def test_post_tiered_rate_rule_with_null_variable_name():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_valid_tiered_rate_rule():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['rule_id'] is not None

    rule_id = response.data['rule_id']
    rule = TieredRateRule.objects.get(pk=rule_id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


# Tiered rate rule updates


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_null_data():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    rule_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/'
    request_url = request_url + str(rule.ruleset.id) + '/rules/'
    request_url = request_url + str(rule_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_null_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(None) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_non_existent_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(479) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_non_numeric_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str('ABC') + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_null_name():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = None
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_null_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = None
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_non_numeric_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 'ABC'
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_nulL_explainer():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 2
    explainer = None
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    rule = TieredRateRule.objects.get(pk=rule.id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


@pytest.mark.django_db
def test_put_tiered_rate_rule_with_null_variable_name():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = None

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_valid_tiered_rate_rule():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())

    assert rule is not None
    assert rule.variable_name == 'salary'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    rule = TieredRateRule.objects.get(pk=rule.id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


# Rule tier creation


@pytest.mark.django_db
def test_post_rule_tier_with_null_data():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = None
    rule_id = None
    min_value = None
    max_value = None
    ordinal = None
    tier_rate = None

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_rule_tier_with_null_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = None
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_rule_tier_with_non_existent_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = 479
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = 'ABC'
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_rule_tier_with_null_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = None
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 'ABC'
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_rule_tier_with_null_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = None
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 'ABC'
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_rule_tier_with_null_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = None
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 'ABC'
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_rule_tier_with_null_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = None

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_rule_tier_with_non_numeric_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 'ABC'

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_valid_rule_tier():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['tier_id'] is not None

    tier_id = response.data['tier_id']
    tier = RuleTier.objects.get(pk=tier_id)

    assert tier.rule.id == rule_id
    assert tier.min_value == min_value
    assert tier.max_value == max_value
    assert tier.ordinal == ordinal
    assert tier.tier_rate == tier_rate


# Rule tier updates


@pytest.mark.django_db
def test_put_rule_tier_with_null_data():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20
    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )
    tier_id = None

    min_value = None
    max_value = None
    ordinal = None
    tier_rate = None

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_rule_tier_with_null_tier_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )
    tier_id = None

    min_value = 9000
    max_value = 50000
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_rule_tier_with_non_existent_tier_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )
    tier_id = 479

    min_value = 9000
    max_value = 50000
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_rule_tier_with_non_numeric_tier_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )
    tier_id = 'tier.id'

    min_value = 9000
    max_value = 50000
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_rule_tier_with_null_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = None
    max_value = 50000
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_rule_tier_with_non_numeric_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 'abc'
    max_value = 50000
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_rule_tier_with_null_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = None
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200


@pytest.mark.django_db
def test_put_rule_tier_with_non_numeric_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = 'abc'
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_rule_tier_with_null_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = 50000
    ordinal = None
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_rule_tier_with_non_numeric_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = 50000
    ordinal = 'abc'
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_rule_tier_with_null_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = 50000
    ordinal = 2
    tier_rate = None

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_rule_tier_with_non_numeric_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = 50000
    ordinal = 2
    tier_rate = 'abc'

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_valid_rule_tier():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    ruleset_id = rule.ruleset.id
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    tier_id = create_rule_tier(
        rule.id,
        min_value,
        max_value,
        ordinal,
        tier_rate
    )

    min_value = 9000
    max_value = 50000
    ordinal = 2
    tier_rate = 25

    body = {
        'min_value': min_value,
        'max_value': max_value,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/tiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    tier = RuleTier.objects.get(pk=tier_id)

    assert tier.min_value == min_value
    assert tier.max_value == max_value
    assert tier.ordinal == ordinal
    assert tier.tier_rate == tier_rate


# Secondary tiered rate rule creation


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_data():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = None
    ruleset_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_ruleset_id():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = None
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_existent_ruleset_id():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = 479
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_numeric_ruleset_id():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = 'ABC'
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_primary_rule_id():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = None
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_existent_primary_rule_id():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = 479
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_numeric_primary_rule_id():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = 'ABC'
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_crete_secondary_tiered_rate_rule_with_null_name():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = primary_rule.ruleset.id
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_ordinal():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_non_numeric_ordinal():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_nulL_explainer():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['rule_id'] is not None

    rule_id = response.data['rule_id']
    rule = SecondaryTieredRateRule.objects.get(pk=rule_id)
    assert rule.primary_rule.id == primary_rule_id
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


@pytest.mark.django_db
def test_post_secondary_tiered_rate_rule_with_null_variable_name():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_valid_secondary_tiered_rate_rule():
    primary_rule = create_mock_simple_tiered_rate_rule(
        9000,
        45000,
        'salary',
        20
    )
    primary_rule_id = primary_rule.id
    ruleset_id = primary_rule.ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'primary_rule_id': primary_rule_id,
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name,
    }

    request_url = url + 'rulesets/' + str(ruleset_id) + '/rules/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['rule_id'] is not None

    rule_id = response.data['rule_id']
    rule = SecondaryTieredRateRule.objects.get(pk=rule_id)
    assert rule.primary_rule.id == primary_rule_id
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


# Secondary tiered rate rule updates


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_null_data():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = None
    ordinal = None
    explainer = None
    variable_name = None

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(None) + '/rules/' + str(None) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_null_rule_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(None) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_non_existent_rule_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(479) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_non_numeric_rule_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str('ABC') + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_iered_rate_rule_with_null_name():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = None
    ordinal = 2
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_null_ordinal():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_non_numeric_ordinal():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_null_explainer():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 2
    explainer = None
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    rule = SecondaryTieredRateRule.objects.get(pk=rule.id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


@pytest.mark.django_db
def test_put_secondary_tiered_rate_rule_with_null_variable_name():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer'
    variable_name = None

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_valid_secondary_tiered_rate_rule():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )

    assert rule is not None
    assert rule.variable_name == 'dividends'

    name = 'Test rule updated'
    ordinal = 2
    explainer = 'Test explainer updated'
    variable_name = 'salary'

    body = {
        'type': 'secondary_tiered_rate',
        'name': name,
        'ordinal': ordinal,
        'explainer': explainer,
        'variable_name': variable_name
    }

    request_url = url + 'rulesets/' + str(rule.ruleset.id)
    request_url = request_url + '/rules/' + str(rule.id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    rule = SecondaryTieredRateRule.objects.get(pk=rule.id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name


# Secondary rule tier creation


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_data():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = None
    rule_id = None
    primary_tier_id = None
    ordinal = None
    tier_rate = None

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_rule_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = None
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_existent_rule_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = 479
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_rule_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = 'ABC'
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_primary_tier_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = None
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_existent_primary_tier_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = 479
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_primary_tier_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = 'ABC'
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_ordinal():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = None
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_ordinal():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 'ABC'
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_null_tier_rate():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = None

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_secondary_rule_tier_with_non_numeric_tier_rate():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 'ABC'

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_valid_secondary_rule_tier():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    body = {
        'primary_tier_id': primary_tier_id,
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data['secondary_tier_id'] is not None

    tier_id = response.data['secondary_tier_id']
    tier = SecondaryRuleTier.objects.get(pk=tier_id)

    assert tier.secondary_rule.id == rule_id
    assert tier.primary_tier.id == primary_tier_id
    assert tier.tier_rate == tier_rate


# Secondary rule tier updates


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_null_data():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = None
    rule_id = None
    ordinal = None
    tier_rate = None

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(None) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_null_tier_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 2
    tier_rate = 30

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(None) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_non_existent_tier_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 2
    tier_rate = 30

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(479) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_non_numeric_tier_id():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    print(str(rule_id))
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 2
    tier_rate = 30

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str('ABC') + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_null_ordinal():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = secondary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = None
    tier_rate = 30

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_non_numeric_ordinal():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = secondary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 'ABC'
    tier_rate = 30

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_null_tier_rate():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = secondary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 2
    tier_rate = None

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_secondary_rule_tier_with_non_numeric_tier_rate():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 'ABC'

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_put_valid_secondary_rule_tier():
    primary_rule = create_mock_tiered_rate_rule(
        'salary',
        1,
        create_mock_ruleset()
    )
    secondary_rule = create_mock_secondary_tiered_rate_rule(
        primary_rule,
        'dividends',
        primary_rule.ruleset
    )
    primary_tier = create_mock_rule_tier(
        primary_rule,
        10000,
        45000,
        20
    )

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 1
    tier_rate = 20

    tier_id = create_secondary_rule_tier(
        rule_id,
        primary_tier_id,
        ordinal,
        tier_rate
    )
    assert tier_id is not None

    ruleset_id = primary_rule.ruleset.id
    rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    ordinal = 2
    tier_rate = 30

    body = {
        'ordinal': ordinal,
        'tax_rate': tier_rate,
    }

    request_url = url + 'rulesets/' + str(ruleset_id)
    request_url = request_url + '/rules/' + str(rule_id)
    request_url = request_url + '/secondarytiers/' + str(tier_id) + '/'
    response = client.put(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200

    tier = SecondaryRuleTier.objects.get(pk=tier_id)

    assert tier.secondary_rule.id == rule_id
    assert tier.tier_rate == tier_rate


# Retrieving calculations


@pytest.mark.django_db
def test_get_calculations_for_null_username():
    body = {
        'username': None,
    }

    request_url = url + 'calculations/?username=' + str(None)
    response = client.get(request_url)

    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_calculations_for_non_existent_username():
    request_url = url + 'calculations/?username=jimbo'
    response = client.get(request_url)

    assert response is not None
    assert response.status_code == 404


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

    request_url = url + 'calculations/?username=bob'
    response = client.get(request_url)

    assert response is not None
    assert response.status_code == 200

    print(response.data)
    assert len(response.data) == 1
    calculation = response.data[0]
    assert calculation['username'] == 'bob'
    assert len(calculation['jurisdictions']) == 1


# Generating calculations


@pytest.mark.django_db
def test_create_calculation_with_no_jurisdictions():
    username = 'bob'
    jurisdiction_ids = []
    variables = create_mock_variable_table()

    body = {
        'username': username,
        'jurisdiction_ids': jurisdiction_ids,
        'variables': variables,
    }

    request_url = url + 'calculations/'
    response = client.post(request_url, body, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_calculation_with_single_jurisdiction():
    rule = create_mock_simple_tiered_rate_rule(8000, 45000, 'salary', 20)
    username = 'bob'
    jurisdiction_ids = [rule.ruleset.jurisdiction_id]
    variables = create_mock_variable_table()

    body = {
        'username': username,
        'jurisdiction_ids': jurisdiction_ids,
        'variables': variables,
    }

    request_url = url + 'calculations/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    assert response.data is not None
    calculation = response.data
    assert len(calculation['jurisdictions']) == 1
    jurisdiction_results = calculation['jurisdictions'][jurisdiction_ids[0]]
    assert len(jurisdiction_results) == 1
    tier_result = jurisdiction_results[0]
    tax_payable = tier_result['tax_payable']

    assert tax_payable == round(1000 * (20/100), 2)


@pytest.mark.django_db
def test_create_calculation_with_multiple_single_rule_jurisdictions():
    rule1 = create_mock_simple_tiered_rate_rule(8000, 45000, 'salary', 20)
    jursdiction_id_1 = rule1.ruleset.jurisdiction_id

    rule2 = create_mock_flat_rate_Rule('dividends', 8, create_mock_ruleset())
    jursdiction_id_2 = rule2.ruleset.jurisdiction_id

    username = 'bob'
    jurisdiction_ids = [jursdiction_id_1, jursdiction_id_2]
    variables = create_mock_variable_table()

    body = {
        'username': username,
        'jurisdiction_ids': jurisdiction_ids,
        'variables': variables,
    }

    request_url = url + 'calculations/'
    response = client.post(request_url, body, format='json')

    assert response is not None
    assert response.status_code == 200
    print(response.data)
    assert response.data is not None
    calculation = response.data

    assert len(calculation['jurisdictions']) == 2
    jurisdiction1_results = calculation['jurisdictions'][jurisdiction_ids[0]]
    jurisdiction2_results = calculation['jurisdictions'][jurisdiction_ids[1]]

    assert len(jurisdiction1_results) == 1
    tier_result = jurisdiction1_results[0]
    tax_payable = tier_result['tax_payable']
    assert tax_payable == round(1000 * 0.2, 2)

    assert len(jurisdiction2_results) == 1
    tier_result = jurisdiction2_results[0]
    tax_payable = tier_result['tax_payable']
    assert tax_payable == round(variables['dividends'] * (8/100), 2)
