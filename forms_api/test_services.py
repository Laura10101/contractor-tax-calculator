from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import *
from .services import *
import pytest


# Create your tests here.
# Test creation of forms
@pytest.mark.django_db
def test_create_form():
    jurisdiction_id = 1
    id = create_form(jurisdiction_id)
    assert id is not None

    form = Form.objects.get(pk=id)
    assert form.jurisdiction_id == jurisdiction_id

def test_create_second_form_for_jurisdiction():
    jurisdiction_id = 1
    id = create_form(jurisdiction_id)
    assert id is not None

    form = Form.objects.get(pk=id)
    assert form.jurisdiction_id == jurisdiction_id

    with pytest.raises(IntegrityError):
        id = create_form(jurisdiction_id)

def test_create_form_with_null_jurisdiction_id():
    jurisdiction_id = None
    with pytest.raises(IntegrityError):
        id = create_form(jurisdiction_id)

def test_create_form_with_non_numeric_jurisdiction_id():
    jurisdiction_id = 'ABC'
    with pytest.raises(ValidationError):
        id = create_form(jurisdiction_id)

# Test retrieval of forms based on jurisdiction IDs
def test_get_forms_with_null_jurisdiction_ids_list():
    jurisdiction_ids = None
    with pytest.raises(Exception):
        forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)

def test_get_forms_with_empty_jurisdiction_ids_list():
    jurisdiction_ids = []
    with pytest.raises(Exception):
        forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)

def test_get_forms_with_non_numeric_jurisdiction_ids_in_list():
    jurisdiction_ids = ['A']
    with pytest.raises(Exception):
        forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)

def test_get_single_form():
    id = create_form(1)
    assert id is not None
    jurisdiction_ids = [1]
    
    forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)
    assert forms is not None
    assert forms.count() == len(jurisdiction_ids)
    assert forms.first().id == id

def test_get_multiple_forms():
    id1 = create_form(1)
    assert id1 is not None

    id2 = create_form(2)
    assert id2 is not None
    jurisdiction_ids = [1,2]
    
    forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)
    assert forms is not None
    assert forms.count() == len(jurisdiction_ids)
    assert forms.first().id == id1

    assert forms[1].id == id2

# Test deletion of forms
def test_delete_form():
    assert Form.objects.all().count() == 0
    id = create_form(1)
    assert id is not None
    jurisdiction_ids = [1]
    
    forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)
    assert forms is not None
    assert forms.count() == len(jurisdiction_ids)
    assert forms.first().id == id

    delete_form(id)
    assert Form.objects.all().count() == 0

def test_delete_form_with_non_existent_id():
    with pytest.raises(ObjectDoesNotExist):
        delete_form(78)

# Test creation of boolean questions
def test_create_boolean_question_with_null_data():
    pass

def test_create_boolean_question_with_null_form_id():
    pass

def test_create_boolean_question_with_non_existent_form_id():
    pass

def test_create_boolean_question_with_null_text():
    pass

def test_create_boolean_question_with_null_ordinal():
    pass

def test_create_boolean_question_with_non_numeric_ordinal():
    pass

def test_create_boolean_question_with_null_explainer():
    pass

def test_create_boolean_question_with_null_is_mandatory():
    pass

def test_create_boolean_question():
    pass

# Test updates to boolean questions
def test_update_boolean_question_with_null_data():
    pass

def test_update_boolean_question_with_null_form_id():
    pass

def test_update_boolean_question_with_non_existent_form_id():
    pass

def test_update_boolean_question_with_null_text():
    pass

def test_update_boolean_question_with_null_ordinal():
    pass

def test_update_boolean_question_with_non_numeric_ordinal():
    pass

def test_update_boolean_question_with_null_explainer():
    pass

def test_update_boolean_question_with_null_is_mandatory():
    pass

def test_update_boolean_question():
    pass

def test_update_boolean_question_with_non_existent_id():
    pass

# Test creation of multiple_choice questions
def test_create_multiple_choice_question_with_null_data():
    pass

def test_create_multiple_choice_question_with_null_form_id():
    pass

def test_create_multiple_choice_question_with_non_existent_form_id():
    pass

def test_create_multiple_choice_question_with_null_text():
    pass

def test_create_multiple_choice_question_with_null_ordinal():
    pass

def test_create_multiple_choice_question_with_non_numeric_ordinal():
    pass

def test_create_multiple_choice_question_with_null_explainer():
    pass

def test_create_multiple_choice_question_with_null_is_mandatory():
    pass

def test_create_multiple_choice_question():
    pass

# Test updates to multiple_choice questions
def test_update_multiple_choice_question_with_null_data():
    pass

def test_update_multiple_choice_question_with_null_form_id():
    pass

def test_update_multiple_choice_question_with_non_existent_form_id():
    pass

def test_update_multiple_choice_question_with_null_text():
    pass

def test_update_multiple_choice_question_with_null_ordinal():
    pass

def test_update_multiple_choice_question_with_non_numeric_ordinal():
    pass

def test_update_multiple_choice_question_with_null_explainer():
    pass

def test_update_multiple_choice_question_with_null_is_mandatory():
    pass

def test_update_multiple_choice_question():
    pass

def test_update_multiple_choice_question_with_non_existent_id():
    pass

# Test creation of numeric questions
def test_create_numeric_question_with_null_data():
    pass

def test_create_numeric_question_with_null_form_id():
    pass

def test_create_numeric_question_with_non_existent_form_id():
    pass

def test_create_numeric_question_with_null_text():
    pass

def test_create_numeric_question_with_null_ordinal():
    pass

def test_create_numeric_question_with_non_numeric_ordinal():
    pass

def test_create_numeric_question_with_null_explainer():
    pass

def test_create_numeric_question_with_null_is_mandatory():
    pass

def test_create_numeric_question_with_null_is_integer():
    pass

def test_create_numeric_question_with_non_boolean_is_integer():
    pass

def test_create_numeric_question_with_null_max_value():
    pass

def test_create_numeric_question_with_non_numeric_max_value():
    pass

def test_create_numeric_question_with_null_min_value():
    pass

def test_create_numeric_question_with_non_numeric_min_value():
    pass

def test_create_numeric_question():
    pass

# Test updates to numeric questions
def test_update_numeric_question_with_null_data():
    pass

def test_update_numeric_question_with_null_form_id():
    pass

def test_update_numeric_question_with_non_existent_form_id():
    pass

def test_update_numeric_question_with_null_text():
    pass

def test_update_numeric_question_with_null_ordinal():
    pass

def test_update_numeric_question_with_non_numeric_ordinal():
    pass

def test_update_numeric_question_with_null_explainer():
    pass

def test_update_numeric_question_with_null_is_mandatory():
    pass

def test_update_numeric_question_with_null_is_integer():
    pass

def test_update_numeric_question_with_non_boolean_is_integer():
    pass

def test_update_numeric_question_with_null_max_value():
    pass

def test_update_numeric_question_with_non_numeric_max_value():
    pass

def test_update_numeric_question_with_null_min_value():
    pass

def test_update_numeric_question_with_non_numeric_min_value():
    pass

def test_update_numeric_question():
    pass

def test_update_numeric_question_with_non_existent_id():
    pass

# Test deleting questions
def test_delete_question():
    form_id = create_form(1)
    assert form_id is not None
    assert Question.objects.all().count() == 0
    id = create_boolean_question(
        form_id,
        'My question is wonderful?',
        1,
        'A test question only',
        False
    )

    delete_question(id)
    assert Form.objects.all().count() == 0

def test_delete_question_with_non_existent_id():
    with pytest.raises(ObjectDoesNotExist):
        delete_question(729)

# Test creation of multiple choice options
def test_create_option_with_null_text():
    pass

def test_create_option():
    pass

# Test deletion of multiple choice options
def test_delete_option():
    pass

def test_delete_option_with_non_existent_id():
    pass