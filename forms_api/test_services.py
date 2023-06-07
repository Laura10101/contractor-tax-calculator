from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest


# Create your tests here.
# Test creation of forms
@pytest.mark.django_db
def test_create_form():
    pass

def test_create_second_form_for_jurisdiction():
    pass

def test_create_form_with_null_jurisdiction_id():
    pass

def test_create_form_with_non_numeric_jurisdiction_id():
    pass

# Test retrieval of forms based on jurisdiction IDs
def test_get_forms_with_null_jurisdiction_ids_list():
    pass

def test_get_forms_with_empty_jurisdiction_ids_list():
    pass

def test_get_forms_with_non_numeric_jurisdiction_ids_in_list():
    pass

def test_get_single_form():
    pass

def test_get_multiple_forms():
    pass

# Test deletion of forms
def test_delete_form():
    pass

def test_delete_form_with_non_existent_id():
    pass

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
    pass

def test_delete_question_with_non_existent_id():
    pass

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