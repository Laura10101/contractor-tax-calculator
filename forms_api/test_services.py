"""Test forms API services."""

from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import *
from .services import *
import pytest


@pytest.mark.django_db
def test_create_form():
    """Test creation of a new form."""

    jurisdiction_id = 1
    id = create_form(jurisdiction_id)
    assert id is not None

    form = Form.objects.get(pk=id)
    assert form.jurisdiction_id == jurisdiction_id


@pytest.mark.django_db
def test_create_second_form_for_jurisdiction():
    """Test creation of a duplicate form."""

    jurisdiction_id = 1
    id = create_form(jurisdiction_id)
    assert id is not None

    form = Form.objects.get(pk=id)
    assert form.jurisdiction_id == jurisdiction_id

    with pytest.raises(ValidationError):
        print('Creating second')
        id = create_form(jurisdiction_id)
        print('Second created')


@pytest.mark.django_db
def test_create_form_with_null_jurisdiction_id():
    """Test creation of a form with null data."""
    jurisdiction_id = None
    with pytest.raises(ValidationError):
        id = create_form(jurisdiction_id)


@pytest.mark.django_db
def test_create_form_with_non_numeric_jurisdiction_id():
    """Test creation of a form with non-numeric data."""
    jurisdiction_id = 'ABC'
    with pytest.raises(ValidationError):
        id = create_form(jurisdiction_id)


@pytest.mark.django_db
def test_get_forms_with_null_jurisdiction_ids_list():
    """Test retrieving a form with null jurisdiction Ids."""
    jurisdiction_ids = None
    with pytest.raises(ValidationError):
        forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)


@pytest.mark.django_db
def test_get_forms_with_empty_jurisdiction_ids_list():
    """Test retrieving forms with an empty jurisdiction ID list."""
    jurisdiction_ids = []
    with pytest.raises(ValidationError):
        forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)


@pytest.mark.django_db
def test_get_forms_with_non_numeric_jurisdiction_ids_in_list():
    """Test retrieving forms with non-numeric jurisdiction IDs."""
    jurisdiction_ids = ['A']
    with pytest.raises(ValidationError):
        forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)


@pytest.mark.django_db
def test_get_single_form():
    id = create_form(1)
    assert id is not None
    jurisdiction_ids = [1]

    forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)
    assert forms is not None
    assert forms.count() == len(jurisdiction_ids)
    assert forms.first().id == id


@pytest.mark.django_db
def test_get_multiple_forms():
    id1 = create_form(1)
    assert id1 is not None

    id2 = create_form(2)
    assert id2 is not None
    jurisdiction_ids = [1, 2]

    forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)
    assert forms is not None
    assert forms.count() == len(jurisdiction_ids)
    assert forms.first().id == id1

    assert forms[1].id == id2


@pytest.mark.django_db
def test_delete_form():
    assert Form.objects.all().count() == 0
    id = create_form(1)
    assert id is not None
    jurisdiction_ids = [1]

    forms = get_forms_by_jurisdiction_ids(jurisdiction_ids)
    assert forms is not None
    assert forms.count() == len(jurisdiction_ids)
    assert forms.first().id == id

    for jurisdiction_id in jurisdiction_ids:
        delete_form_for_jurisdiction(jurisdiction_id)
    assert Form.objects.all().count() == 0


def get_mock_form():
    jurisdiction_id = 1
    form_id = create_form(jurisdiction_id)
    return form_id


def get_mock_multiple_choice_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )
    return id


@pytest.mark.django_db
def test_create_boolean_question_with_null_data():
    form_id = get_mock_form()
    question_text = None
    ordinal = None
    explainer = None
    variable_name = None
    is_mandatory = None

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_null_form_id():
    form_id = None
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_non_existent_form_id():
    form_id = 7256
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(Form.DoesNotExist):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_non_numeric_form_id():
    form_id = 'Wrongo'
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_null_text():
    form_id = get_mock_form()
    question_text = None
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = None
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 'Try again'
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = None
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_null_variable_name():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = None
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_blank_variable_name():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = ''
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = None

    with pytest.raises(ValidationError):
        id = create_boolean_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_boolean_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )
    assert id is not None
    question = BooleanQuestion.objects.get(pk=id)
    assert question.text == question_text
    assert question.ordinal == ordinal
    assert question.explainer == explainer
    assert question.is_mandatory == is_mandatory


@pytest.mark.django_db
def test_update_boolean_question_with_null_data():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )
    new_text = None
    new_ordinal = None
    new_explainer = None
    new_is_mandatory = None

    with pytest.raises(ValidationError):
        update_boolean_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_boolean_question_with_null_text():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = None
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_boolean_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_boolean_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = None
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_boolean_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_boolean_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 'Hmmm'
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_boolean_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_boolean_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = None
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_boolean_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_boolean_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = None

    with pytest.raises(ValidationError):
        update_boolean_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_boolean_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    update_boolean_question(
        id,
        new_text,
        new_ordinal,
        new_explainer,
        new_is_mandatory
    )

    question = BooleanQuestion.objects.get(pk=id)
    assert question is not None
    assert question.text == new_text
    assert question.ordinal == new_ordinal
    assert question.explainer == new_explainer
    assert question.is_mandatory == new_is_mandatory


@pytest.mark.django_db
def test_update_boolean_question_with_non_existent_id():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_boolean_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ObjectDoesNotExist):
        update_boolean_question(
            7236,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_data():
    form_id = get_mock_form()
    question_text = None
    ordinal = None
    explainer = None
    variable_name = None
    is_mandatory = None

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_form_id():
    form_id = None
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_non_existent_form_id():
    form_id = 7256
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(Form.DoesNotExist):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_non_numeric_form_id():
    form_id = 'Wrongo'
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_text():
    form_id = get_mock_form()
    question_text = None
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = None
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 'Try again'
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = None
    variable_name = 'fake_var_name'
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_variable_name():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = None
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_blank_variable_name():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = ''
    is_mandatory = True

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = None

    with pytest.raises(ValidationError):
        id = create_multiple_choice_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory
        )


@pytest.mark.django_db
def test_create_multiple_choice_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )
    assert id is not None
    question = MultipleChoiceQuestion.objects.get(pk=id)
    assert question.text == question_text
    assert question.ordinal == ordinal
    assert question.explainer == explainer
    assert question.is_mandatory == is_mandatory


@pytest.mark.django_db
def test_update_multiple_choice_question_with_null_data():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = None
    new_ordinal = None
    new_explainer = None
    new_is_mandatory = None

    with pytest.raises(ValidationError):
        update_multiple_choice_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_multiple_choice_question_with_null_text():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = None
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_multiple_choice_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_multiple_choice_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = None
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_multiple_choice_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_multiple_choice_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 'Hmmm'
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_multiple_choice_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_multiple_choice_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = None
    new_is_mandatory = False

    with pytest.raises(ValidationError):
        update_multiple_choice_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_multiple_choice_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = None

    with pytest.raises(ValidationError):
        update_multiple_choice_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_update_multiple_choice_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    update_multiple_choice_question(
        id,
        new_text,
        new_ordinal,
        new_explainer,
        new_is_mandatory
    )

    question = MultipleChoiceQuestion.objects.get(pk=id)
    assert question is not None
    assert question.text == new_text
    assert question.ordinal == new_ordinal
    assert question.explainer == new_explainer
    assert question.is_mandatory == new_is_mandatory


@pytest.mark.django_db
def test_update_multiple_choice_question_with_non_existent_id():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True

    id = create_multiple_choice_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False

    with pytest.raises(ObjectDoesNotExist):
        update_multiple_choice_question(
            7236,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_data():
    form_id = get_mock_form()
    question_text = None
    ordinal = None
    explainer = None
    variable_name = None
    is_mandatory = None
    is_integer = None
    min_value = None
    max_value = None

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_form_id():
    form_id = None
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_non_existent_form_id():
    form_id = 7256
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(Form.DoesNotExist):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_non_numeric_form_id():
    form_id = 'Wrongo'
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_text():
    form_id = get_mock_form()
    question_text = None
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = None
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 'Try again'
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = None
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_variable_name():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = None
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_blank_variable_name():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = ''
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = None
    is_integer = False
    min_value = 0
    max_value = 100

    with pytest.raises(ValidationError):
        id = create_numeric_question(
            form_id,
            question_text,
            ordinal,
            explainer,
            variable_name,
            is_mandatory,
            is_integer,
            min_value,
            max_value
        )


@pytest.mark.django_db
def test_create_numeric_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )
    assert id is not None
    question = NumericQuestion.objects.get(pk=id)
    assert question.text == question_text
    assert question.ordinal == ordinal
    assert question.explainer == explainer
    assert question.is_mandatory == is_mandatory


@pytest.mark.django_db
def test_update_numeric_question_with_null_data():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = None
    new_ordinal = None
    new_explainer = None
    new_is_mandatory = None
    new_is_integer = None
    new_min_val = None
    new_max_val = None

    with pytest.raises(ValidationError):
        update_numeric_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_update_numeric_question_with_null_text():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = None
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    with pytest.raises(ValidationError):
        update_numeric_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_update_numeric_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = None
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    with pytest.raises(ValidationError):
        update_numeric_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_update_numeric_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 'Hmmm'
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    with pytest.raises(ValidationError):
        update_numeric_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_update_numeric_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = None
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    with pytest.raises(ValidationError):
        update_numeric_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_update_numeric_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = None
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    with pytest.raises(ValidationError):
        update_numeric_question(
            id,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_update_numeric_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    update_numeric_question(
        id,
        new_text,
        new_ordinal,
        new_explainer,
        new_is_mandatory,
        new_is_integer,
        new_min_val,
        new_max_val
    )

    question = NumericQuestion.objects.get(pk=id)
    assert question is not None
    assert question.text == new_text
    assert question.ordinal == new_ordinal
    assert question.explainer == new_explainer
    assert question.is_mandatory == new_is_mandatory
    assert question.is_integer == new_is_integer
    assert question.min_value == new_min_val
    assert question.max_value == new_max_val


@pytest.mark.django_db
def test_update_numeric_question_with_non_existent_id():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    variable_name = 'fake_var_name'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(
        form_id,
        question_text,
        ordinal,
        explainer,
        variable_name,
        is_mandatory,
        is_integer,
        min_value,
        max_value
    )

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    with pytest.raises(ObjectDoesNotExist):
        update_numeric_question(
            4894,
            new_text,
            new_ordinal,
            new_explainer,
            new_is_mandatory,
            new_is_integer,
            new_min_val,
            new_max_val
        )


@pytest.mark.django_db
def test_delete_question():
    form_id = create_form(1)
    assert form_id is not None
    assert Question.objects.all().count() == 0
    id = create_boolean_question(
        form_id,
        'My question is wonderful?',
        1,
        'A test question only',
        'var_name',
        False
    )

    delete_question(id)
    assert Question.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_question_with_non_existent_id():
    with pytest.raises(ObjectDoesNotExist):
        delete_question(729)


@pytest.mark.django_db
def test_create_option_with_null_text():
    question_id = get_mock_multiple_choice_question()
    text = None
    explainer = None
    with pytest.raises(ValidationError):
        id = create_multiple_choice_option(
            question_id,
            text, explainer
        )


@pytest.mark.django_db
def test_create_option():
    question_id = get_mock_multiple_choice_question()
    text = 'Fried'
    explainer = 'In lots of oil'
    id = create_multiple_choice_option(question_id, text, explainer)
    assert id is not None
    option = MultipleChoiceOption.objects.get(pk=id)
    assert option.question.id == question_id
    assert option.text == text
    assert option.explainer == explainer


# Test deletion of multiple choice options
@pytest.mark.django_db
def test_delete_option():
    assert MultipleChoiceOption.objects.all().count() == 0
    question_id = get_mock_multiple_choice_question()
    text = 'Fried'
    explainer = 'In lots of oil'
    id = create_multiple_choice_option(question_id, text, explainer)
    option = MultipleChoiceOption.objects.get(pk=id)
    assert option.text == text
    assert MultipleChoiceOption.objects.all().count() == 1
    delete_multiple_choice_option(id)
    assert MultipleChoiceOption.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_option_with_non_existent_id():
    with pytest.raises(MultipleChoiceOption.DoesNotExist):
        delete_multiple_choice_option(7496854)
