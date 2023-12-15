from .models import *
from .test_models import *
from .services import *
from .views import *
from django.core.exceptions import ValidationError
import pytest

# Ruleset creation
@pytest.mark.django_db
def test_create_ruleset_with_null_data():
    jurisdiction_id = None
    tax_category_id = None
    with pytest.raises(ValidationError):
        id = create_ruleset(jurisdiction_id, tax_category_id)
        
@pytest.mark.django_db
def test_create_ruleset_with_null_jurisdiction_id():
    jurisdiction_id = None
    tax_category_id = TaxCategory.objects.create(name='Test Category').id
    
    with pytest.raises(ValidationError):
        id = create_ruleset(jurisdiction_id, tax_category_id)

@pytest.mark.django_db
def test_create_ruleset_with_null_tax_category_id():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = None
    
    with pytest.raises(TaxCategory.DoesNotExist):
        id = create_ruleset(jurisdiction_id, tax_category_id)

@pytest.mark.django_db
def test_create_ruleset_with_non_existent_tax_category_id():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = 479
    
    with pytest.raises(TaxCategory.DoesNotExist):
        id = create_ruleset(jurisdiction_id, tax_category_id)

@pytest.mark.django_db
def test_create_ruleset_with_duplicate_tax_category_jurisdiction_combination():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = TaxCategory.objects.create(name='Test Category').id
    
    id = create_ruleset(jurisdiction_id, tax_category_id)
    
    with pytest.raises(ValidationError):
        id = create_ruleset(jurisdiction_id, tax_category_id)

@pytest.mark.django_db
def test_create_valid_ruleset():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = TaxCategory.objects.create(name='Test Category').id
    
    id = create_ruleset(jurisdiction_id, tax_category_id)
    
    assert id is not None
    ruleset = RuleSet.objects.get(pk=id)
    assert ruleset.jurisdiction_id == jurisdiction_id
    assert ruleset.tax_category.id == tax_category_id

# Ruleset deletion
@pytest.mark.django_db
def test_delete_ruleset_with_null_id():
    with pytest.raises(RuleSet.DoesNotExist):
        delete_ruleset(None)

@pytest.mark.django_db
def test_delete_ruleset_with_non_existent_id():
    with pytest.raises(RuleSet.DoesNotExist):
        delete_ruleset(479)

@pytest.mark.django_db
def test_delete_ruleset():
    jurisdiction_id = create_mock_jurisdiction().id
    tax_category_id = TaxCategory.objects.create(name='Test Category').id
    
    id = create_ruleset(jurisdiction_id, tax_category_id)
    
    assert id is not None
    ruleset = RuleSet.objects.get(pk=id)
    assert ruleset.jurisdiction_id == jurisdiction_id
    assert ruleset.tax_category.id == tax_category_id

    delete_ruleset(id)

    assert id is not None
    with pytest.raises(RuleSet.DoesNotExist):
        ruleset = RuleSet.objects.get(pk=id)

# Tax category creation
@pytest.mark.django_db
def test_create_tax_category_with_null_name():
    name = None
    with pytest.raises(ValidationError):
        id = create_tax_category(name)

@pytest.mark.django_db
def test_create_tax_category_with_duplicate_name():
    name = 'Test Category'
    create_tax_category(name)
    
    with pytest.raises(ValidationError):
        id = create_tax_category(name)

@pytest.mark.django_db
def test_create_valid_tax_category():
    name = 'Test Category'
    id = create_tax_category(name)

    assert id is not None

    category = TaxCategory.objects.get(pk=id)
    assert category.name == name

#  Tax category deletion
@pytest.mark.django_db
def test_delete_tax_category_with_null_id():
    with pytest.raises(TaxCategory.DoesNotExist):
        delete_tax_category(None)

@pytest.mark.django_db
def test_delete_tax_category_with_non_existent_id():
    with pytest.raises(TaxCategory.DoesNotExist):
        delete_tax_category(479)

@pytest.mark.django_db
def test_delete_tax_category():
    name = 'Test Category'
    id = create_tax_category(name)

    assert id is not None

    category = TaxCategory.objects.get(pk=id)
    assert category.name == name

    delete_tax_category(id)

    with pytest.raises(TaxCategory.DoesNotExist):
        category = TaxCategory.objects.get(pk=id)

# Rule deletion
@pytest.mark.django_db
def test_delete_rule_with_null_id():
    with pytest.raises(Rule.DoesNotExist):
        delete_rule(None)

@pytest.mark.django_db
def test_delete_rule_with_non_existent_id():
    with pytest.raises(Rule.DoesNotExist):
        delete_rule(479)

@pytest.mark.django_db
def test_delete_rule():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset())
    assert rule_id is not None
    rule = FlatRateRule.objects.get(pk=rule_id)
    assert rule is not None
    assert rule.variable_name == 'salary'
    delete_rule(rule_id)
    with pytest.raises(FlatRateRule.DoesNotExist):
        rule = FlatRateRule.objects.get(pk=rule_id)

# Flat rate rule creation
@pytest.mark.django_db
def test_create_flat_rate_rule_with_null_data():
    ruleset_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None
    flat_rate = None

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_null_ruleset_id():
    ruleset_id = None
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_non_existent_ruleset_id():
    ruleset_id = 479
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_non_numeric_ruleset_id():
    ruleset_id = 'ABC'
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_crete_flat_rate_rule_with_null_name():
    ruleset_id = create_mock_ruleset().id
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_null_ordinal():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_non_numeric_ordinal():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_nulL_explainer():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'
    flat_rate = 20

    id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)
    
    assert id is not None
    rule = FlatRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate

@pytest.mark.django_db
def test_create_flat_rate_rule_with_null_variable_name():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None
    flat_rate = 20

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_null_flat_rate():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = None

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_non_numeric_flat_rate():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 'ABC'

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_flat_rate_rule_with_negative_flat_rate():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = -20

    with pytest.raises(ValidationError):
        id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_create_valid_flat_rate_rule():
    ruleset_id = create_mock_ruleset().id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    id = create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, flat_rate)
    
    assert id is not None
    rule = FlatRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate

# Flat rate rule updates
@pytest.mark.django_db
def test_update_flat_rate_rule_with_null_data():
    rule_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None
    flat_rate = None

    with pytest.raises(FlatRateRule.DoesNotExist):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_null_rule_id():
    rule_id = None
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(FlatRateRule.DoesNotExist):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_non_existent_rule_id():
    rule_id = 479
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(FlatRateRule.DoesNotExist):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_non_numeric_rule_id():
    rule_id = 'ABC'
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(FlatRateRule.DoesNotExist):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_null_name():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_null_ordinal():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_non_numeric_ordinal():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_nulL_explainer():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'
    flat_rate = 20

    update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

    rule = FlatRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate

@pytest.mark.django_db
def test_update_flat_rate_rule_with_null_variable_name():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None
    flat_rate = 20

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_null_flat_rate():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = None

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_non_numeric_flat_rate():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 'ABC'

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_flat_rate_rule_with_negative_flat_rate():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = -20

    with pytest.raises(ValidationError):
        update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

@pytest.mark.django_db
def test_update_valid_flat_rate_rule():
    rule_id = create_mock_flat_rate_Rule('salary', 20, create_mock_ruleset()).id
    assert rule_id is not None

    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'
    flat_rate = 20

    update_flat_rate_rule(rule_id, name, ordinal, explainer, variable_name, flat_rate)

    rule = FlatRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.variable_name == variable_name
    assert rule.flat_rate == flat_rate


# Tiered rate rule creation
@pytest.mark.django_db
def test_create_tiered_rate_rule_with_null_data():
    ruleset_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_null_ruleset_id():
    ruleset_id = None
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_non_existent_ruleset_id():
    ruleset_id = 479
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_non_numeric_ruleset_id():
    ruleset_id = 'ABC'
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_crete_tiered_rate_rule_with_null_name():
    ruleset_id = create_mock_ruleset()
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(ValidationError):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_null_ordinal():
    ruleset_id = create_mock_ruleset()
    name = 'Test Rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(ValidationError):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_non_numeric_ordinal():
    ruleset_id = create_mock_ruleset()
    name = 'Test Rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(ValidationError):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_nulL_explainer():
    ruleset_id = create_mock_ruleset()
    name = 'Test Rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'

    id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

    assert id is not None

    rule = TieredRateRule.objects.get(id)

    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name

@pytest.mark.django_db
def test_create_tiered_rate_rule_with_null_variable_name():
    ruleset_id = create_mock_ruleset()
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None

    with pytest.raises(ValidationError):
        id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_valid_tiered_rate_rule():
    ruleset_id = create_mock_ruleset()
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)

    assert id is not None

    rule = TieredRateRule.objects.get(id)

    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name

# Tiered rate rule updates
@pytest.mark.django_db
def test_update_tiered_rate_rule_with_null_data():
    ruleset = create_mock_ruleset()
    ruleset_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(TieredRateRule.DoesNotExist):
        update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)


@pytest.mark.django_db
def test_update_tiered_rate_rule_with_null_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = None
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(TieredRateRule.DoesNotExist):
        update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_non_existent_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(TieredRateRule.DoesNotExist):
        update_tiered_rate_rule(479, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_non_numeric_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(TieredRateRule.DoesNotExist):
        update_tiered_rate_rule('ABC', name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_null_name():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_null_ordinal():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_non_numeric_ordinal():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_nulL_explainer():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

    rule = TieredRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.variable_name == variable_name
    assert rule.exlainer == explainer

@pytest.mark.django_db
def test_update_tiered_rate_rule_with_null_variable_name():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_valid_tiered_rate_rule():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name)
    assert id is not None

    update_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

    rule = TieredRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.variable_name == variable_name
    assert rule.exlainer == explainer

# Rule tier creation
@pytest.mark.django_db
def test_create_rule_tier_with_null_data():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = None
    min_value = None
    max_value = None
    ordinal = None
    tier_rate = None

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_null_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = None
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_non_existent_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = 479
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_non_numeric_rule_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = 'ABC'
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_null_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = None
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_non_numeric_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 'ABC'
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_null_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = None
    ordinal = 1
    tier_rate = 20

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_non_numeric_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 'ABC'
    ordinal = 1
    tier_rate = 20

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_null_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = None
    tier_rate = 20

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_non_numeric_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 'ABC'
    tier_rate = 20

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_null_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = None

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_rule_tier_with_non_numeric_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 'ABC'

    with pytest.raises(ValidationError):
        id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_create_valid_rule_tier():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    assert tier.rule.id == rule_id
    assert tier.min_value == min_value
    assert tier.max_value == max_value
    assert tier.ordinal == ordinal
    assert tier.tier_rate == tier_rate

# Rule tier updates
@pytest.mark.django_db
def test_update_rule_tier_with_null_data():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    id = None
    min_value = None
    max_value = None
    ordinal = None
    tier_rate = None

    with pytest.raises(RuleTier.DoesNotExist):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_null_tier_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    id = None
    min_value = 9000
    max_value = 50000
    ordinal = 1
    tier_rate = 25

    with pytest.raises(RuleTier.DoesNotExist):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_non_existent_tier_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    id = 479
    min_value = 9000
    max_value = 50000
    ordinal = 1
    tier_rate = 25

    with pytest.raises(RuleTier.DoesNotExist):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_non_numeric_tier_id():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    id = 'ABC'
    min_value = 9000
    max_value = 50000
    ordinal = 1
    tier_rate = 25

    with pytest.raises(RuleTier.DoesNotExist):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_null_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = None
    max_value = 50000
    ordinal = 1
    tier_rate = 25

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_non_numeric_min_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 'ABC'
    max_value = 50000
    ordinal = 1
    tier_rate = 25

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_null_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = None
    ordinal = 1
    tier_rate = 25

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_non_numeric_max_value():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = 'ABC'
    ordinal = 1
    tier_rate = 25

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_null_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = 50000
    ordinal = None
    tier_rate = 25

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_non_numeric_ordinal():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = 50000
    ordinal = 'ABC'
    tier_rate = 25

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_null_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = 50000
    ordinal = 1
    tier_rate = None

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_rule_tier_with_non_numeric_tier_rate():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = 50000
    ordinal = 1
    tier_rate = 'ABC'

    with pytest.raises(ValidationError):
        update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

@pytest.mark.django_db
def test_update_valid_rule_tier():
    rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    rule_id = rule.id
    min_value = 10000
    max_value = 45000
    ordinal = 1
    tier_rate = 20

    id = create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate)
    assert id is not None

    tier = RuleTier.objects.get(pk=id)
    assert tier is not None

    min_value = 9000
    max_value = 50000
    ordinal = 1
    tier_rate = 25

    update_rule_tier(id, min_value, max_value, ordinal, tier_rate)

    assert tier.min_value == min_value
    assert tier.max_value == max_value
    assert tier.ordinal == ordinal
    assert tier.tier_rate == tier_rate

# Secondary tiered rate rule creation
@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_null_data():
    ruleset = create_mock_ruleset()
    ruleset_id = None
    primary_rule_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_null_ruleset_id():
    ruleset = create_mock_ruleset()
    ruleset_id = None
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_non_existent_ruleset_id():
    ruleset = create_mock_ruleset()
    ruleset_id = 479
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_non_numeric_ruleset_id():
    ruleset = create_mock_ruleset()
    ruleset_id = 'ABC'
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(RuleSet.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_null_primary_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = None
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_non_existent_primary_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = 479
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_non_numeric_primary_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = 'ABC'
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(TieredRateRule.DoesNotExist):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_crete_secondary_tiered_rate_rule_with_null_name():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(ValidationError):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_null_ordinal():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(ValidationError):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_non_numeric_ordinal():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    with pytest.raises(ValidationError):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_nulL_explainer():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'

    id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

    assert id is not None

    rule = SecondaryTieredRateRule.objects.get(id)

    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name

@pytest.mark.django_db
def test_create_secondary_tiered_rate_rule_with_null_variable_name():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None

    with pytest.raises(ValidationError):
        id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_create_valid_secondary_tiered_rate_rule():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('Test Tiered Rule', 1, ruleset).id
    name = 'Test Rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)

    assert id is not None

    rule = SecondaryTieredRateRule.objects.get(id)

    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.explainer == explainer
    assert rule.variable_name == variable_name

# Secondary tiered rate rule updates
@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_null_data():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = None
    name = None
    ordinal = None
    explainer = None
    variable_name = None

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(RuleSet.DoesNotExist):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_null_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = None
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_non_existent_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = 479
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_non_numeric_rule_id():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = 'ABC'
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_iered_rate_rule_with_null_name():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('salary', 20, ruleset)
    name = None
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_null_ordinal():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('salary', 20, ruleset)
    name = 'Test rule'
    ordinal = None
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_non_numeric_ordinal():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('salary', 20, ruleset)
    name = 'Test rule'
    ordinal = 'ABC'
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_nulL_explainer():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('salary', 1, ruleset)
    name = 'Test rule'
    ordinal = 1
    explainer = None
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

    rule = SecondaryTieredRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.variable_name == variable_name
    assert rule.explainer == explainer


@pytest.mark.django_db
def test_update_secondary_tiered_rate_rule_with_null_variable_name():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('salary', 20, ruleset)
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = None

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    with pytest.raises(ValidationError):
        update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

@pytest.mark.django_db
def test_update_valid_secondary_tiered_rate_rule():
    ruleset = create_mock_ruleset()
    ruleset_id = ruleset.id
    primary_rule_id = create_mock_tiered_rate_rule('salary', 1, ruleset)
    name = 'Test rule'
    ordinal = 1
    explainer = 'Test explainer'
    variable_name = 'salary'

    rule_id = create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name)
    assert id is not None

    update_secondary_tiered_rate_rule(rule_id, name, ordinal, explainer, variable_name)

    rule = SecondaryTieredRateRule.objects.get(pk=id)
    assert rule.name == name
    assert rule.ordinal == ordinal
    assert rule.variable_name == variable_name
    assert rule.explainer == explainer


# Secondary rule tier creation
@pytest.mark.django_db
def test_create_secondary_rule_tier_with_null_data():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = None
    primary_tier_id = None
    tier_rate = None
    
    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_null_rule_id():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = None
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_non_existent_rule_id():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = 479
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_non_numeric_rule_id():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = 'ABC'
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    with pytest.raises(SecondaryTieredRateRule.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_null_primary_tier_id():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = None
    tier_rate = 8
    
    with pytest.raises(RuleTier.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_non_existent_primary_tier_id():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = 479
    tier_rate = 8
    
    with pytest.raises(RuleTier.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_non_numeric_primary_tier_id():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = 'ABC'
    tier_rate = 8
    
    with pytest.raises(RuleTier.DoesNotExist):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_null_tier_rate():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    tier_rate = None
    
    with pytest.raises(ValidationError):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_secondary_rule_tier_with_non_numeric_tier_rate():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    tier_rate = 'ABC'
    
    with pytest.raises(ValidationError):
        id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)

@pytest.mark.django_db
def test_create_valid_secondary_rule_tier():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)
    assert id is not None

    tier = SecondaryRuleTier.objects.get(pk=id)
    assert tier is not None

    assert tier.secondary_rule.id == secondary_rule_id
    assert tier.primary_tier.id == primary_tier_id
    assert tier.tier_rate == tier_rate

# Secondary rule tier updates
@pytest.mark.django_db
def test_update_secondary_rule_tier_with_null_tier_rate():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)
    assert id is not None

    tier = SecondaryRuleTier.objects.get(pk=id)
    assert tier is not None

    tier_rate = None

    with pytest.raises(ValidationError):
        update_secondary_rule_tier(id, tier_rate)

@pytest.mark.django_db
def test_update_secondary_rule_tier_with_non_numeric_tier_rate():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)
    assert id is not None

    tier = SecondaryRuleTier.objects.get(pk=id)
    assert tier is not None

    tier_rate = 'ABC'

    with pytest.raises(ValidationError):
        update_secondary_rule_tier(id, tier_rate)

@pytest.mark.django_db
def test_update_valid_secondary_rule_tier():
    primary_rule = create_mock_tiered_rate_rule('salary', 1, create_mock_ruleset())
    secondary_rule = create_mock_secondary_tiered_rate_rule(primary_rule, 'dividends', primary_rule.ruleset)
    primary_tier = create_mock_rule_tier(primary_rule, 10000, 45000, 20)

    secondary_rule_id = secondary_rule.id
    primary_tier_id = primary_tier.id
    tier_rate = 8
    
    id = create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate)
    assert id is not None

    tier = SecondaryRuleTier.objects.get(pk=id)
    assert tier is not None

    tier_rate = 25

    update_secondary_rule_tier(id, tier_rate)

    tier = SecondaryRuleTier.objects.get(pk=id)
    assert tier.tier_rate == tier_rate
