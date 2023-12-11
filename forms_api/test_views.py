from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import *
from .services import *
from .views import *
import pytest

client = APIClient()
url = '/api/forms/'

# Create your tests here.
# Test creation of jurisdictions
# Test creation of forms
@pytest.mark.django_db
def test_post_form():
    jurisdiction_id = 1

    data = {'jurisdiction_id': jurisdiction_id}
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    id = response.data['form_id']
    assert id is not None

    form = Form.objects.get(pk=id)
    assert form.jurisdiction_id == jurisdiction_id

@pytest.mark.django_db
def test_post_second_form_for_jurisdiction():
    jurisdiction_id = 1
    id = create_form(jurisdiction_id)
    assert id is not None

    form = Form.objects.get(pk=id)
    assert form.jurisdiction_id == jurisdiction_id

    data = {'jurisdiction_id': jurisdiction_id}
    response = client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_form_with_null_jurisdiction_id():
    jurisdiction_id = None
    data = {'jurisdiction_id': jurisdiction_id}
    response = client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_form_with_non_numeric_jurisdiction_id():
    jurisdiction_id = 'ABC'
    data = {'jurisdiction_id': jurisdiction_id}
    response = client.post(url, data, format='json')
    assert response.status_code == 400

# Test retrieval of forms based on jurisdiction IDs
@pytest.mark.django_db
def test_get_forms_with_no_jurisdiction_ids_list():
    jurisdiction_ids = None
    response = client.get(url)
    assert response.status_code == 400

@pytest.mark.django_db
def test_get_forms_with_empty_jurisdiction_ids_list():
    jurisdiction_ids = []
    jurisdiction_id_str = ','.join([str(id) for id in jurisdiction_ids])
    request_url = url + '?ids=' + jurisdiction_id_str
    response = client.get(request_url)
    assert response.status_code == 400

@pytest.mark.django_db
def test_get_forms_with_non_numeric_jurisdiction_ids_in_list():
    jurisdiction_ids = [1,2,3,'A']
    jurisdiction_id_str = ','.join([str(id) for id in jurisdiction_ids])
    request_url = url + '?ids=' + jurisdiction_id_str
    response = client.get(request_url)
    assert response.status_code == 400

@pytest.mark.django_db
def test_get_single_form():
    id = create_form(1)
    assert id is not None
    jurisdiction_ids = [1]
    jurisdiction_id_str = ','.join([str(id) for id in jurisdiction_ids])
    request_url = url + '?jurisdiction_ids=' + jurisdiction_id_str
    print(request_url)
    response = client.get(request_url)
    assert response.status_code == 200

    forms = response.data['forms']

    assert forms is not None
    assert len(forms) == len(jurisdiction_ids)
    assert forms[id]['id'] == id

@pytest.mark.django_db
def test_get_multiple_forms():
    id1 = create_form(1)
    assert id1 is not None

    id2 = create_form(2)
    assert id2 is not None
    jurisdiction_ids = [1,2]
    
    jurisdiction_id_str = ','.join([str(id) for id in jurisdiction_ids])
    request_url = url + '?jurisdiction_ids=' + jurisdiction_id_str
    print(request_url)
    response = client.get(request_url)
    assert response.status_code == 200

    forms = response.data['forms']

    assert forms is not None
    assert len(forms) == len(jurisdiction_ids)
    assert forms[id1]['id'] == id1
    assert forms[id2]['id'] == id2

# Test deletion of forms
@pytest.mark.django_db
def test_delete_form():
    assert Form.objects.all().count() == 0
    id = create_form(1)
    assert id is not None
    jurisdiction_ids = [1]
    
    assert Form.objects.all().count() == 1

    request_url = url + str(id) + '/'
    response = client.delete(request_url)
    assert response.status_code == 200

    assert Form.objects.all().count() == 0

@pytest.mark.django_db
def test_delete_form_with_non_existent_id():
    request_url = url + '456945/'
    response = client.delete(request_url)
    assert response.status_code == 404

# Test creation of boolean questions
# Helper function to create a mock form
def get_mock_form():
    jurisdiction_id = 1
    form_id = create_form(jurisdiction_id)
    return form_id

@pytest.mark.django_db
def test_post_boolean_question_with_null_data():
    form_id = get_mock_form()
    question_text = None
    ordinal = None
    explainer = None
    is_mandatory = None

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_boolean_question_with_null_form_id():
    form_id = None
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_boolean_question_with_non_existent_form_id():
    form_id = 7256
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_boolean_question_with_non_numeric_form_id():
    form_id = 'Wrongo'
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_boolean_question_with_null_text():
    form_id = get_mock_form()
    question_text = None
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_boolean_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = None
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_boolean_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 'Try again'
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_boolean_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = None
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_boolean_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = None

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_boolean_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'boolean',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 200
    id = response.data['id']
    assert id is not None
    question = BooleanQuestion.objects.get(pk=id)
    assert question.text == question_text
    assert question.ordinal == ordinal
    assert question.explainer == explainer
    assert question.is_mandatory == is_mandatory

# Test updates to boolean questions
@pytest.mark.django_db
def test_put_boolean_question_with_null_data():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = None
    new_ordinal = None
    new_explainer = None
    new_is_mandatory = None

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_boolean_question_with_null_text():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = None
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_boolean_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = None
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_boolean_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 'Hmmm'
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_boolean_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = None
    new_is_mandatory = False

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_boolean_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = None

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_boolean_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_boolean_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 200

    question = BooleanQuestion.objects.get(pk=id)
    assert question is not None
    assert question.text == new_text
    assert question.ordinal == new_ordinal
    assert question.explainer == new_explainer
    assert question.is_mandatory == new_is_mandatory

@pytest.mark.django_db
def test_put_boolean_question_with_non_existent_id():
    form_id = get_mock_form()
    id = 8496494
    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'boolean',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 404

# Test creation of multiple_choice questions
@pytest.mark.django_db
def test_post_multiple_choice_question_with_null_data():
    form_id = get_mock_form()
    question_text = None
    ordinal = None
    explainer = None
    is_mandatory = None

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_multiple_choice_question_with_null_form_id():
    form_id = None
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_multiple_choice_question_with_non_existent_form_id():
    form_id = 7256
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_multiple_choice_question_with_non_numeric_form_id():
    form_id = 'Wrongo'
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_multiple_choice_question_with_null_text():
    form_id = get_mock_form()
    question_text = None
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_multiple_choice_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = None
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_multiple_choice_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 'Try again'
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_multiple_choice_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = None
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_multiple_choice_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = None

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_multiple_choice_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True

    data = {
        'type': 'multiple_choice',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 200
    id = response.data['id']
    print('id: ' + str(id))
    print(type(id))
    assert id is not None
    question = MultipleChoiceQuestion.objects.get(pk=id)
    assert question.text == question_text
    assert question.ordinal == ordinal
    assert question.explainer == explainer
    assert question.is_mandatory == is_mandatory

# Test updates to multiple choice questions
@pytest.mark.django_db
def test_put_multiple_choice_question_with_null_data():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = None
    new_ordinal = None
    new_explainer = None
    new_is_mandatory = None

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_multiple_choice_question_with_null_text():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = None
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_multiple_choice_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = None
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_multiple_choice_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 'Hmmm'
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_multiple_choice_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = None
    new_is_mandatory = False

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_multiple_choice_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = None

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_multiple_choice_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    
    id = create_multiple_choice_question(form_id, question_text, ordinal, explainer, is_mandatory)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 200

    question = MultipleChoiceQuestion.objects.get(pk=id)
    assert question is not None
    assert question.text == new_text
    assert question.ordinal == new_ordinal
    assert question.explainer == new_explainer
    assert question.is_mandatory == new_is_mandatory

@pytest.mark.django_db
def test_put_multiple_choice_question_with_non_existent_id():
    form_id = get_mock_form()
    id = 519596
    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False

    data = {
        'type': 'multiple_choice',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 404

# Test creation of numeric questions
@pytest.mark.django_db
def test_post_numeric_question_with_null_data():
    form_id = get_mock_form()
    question_text = None
    ordinal = None
    explainer = None
    is_mandatory = None
    is_integer = None
    min_value = None
    max_value = None

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_numeric_question_with_null_form_id():
    form_id = None
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_numeric_question_with_non_existent_form_id():
    form_id = 7256
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_numeric_question_with_non_numeric_form_id():
    form_id = 'Wrongo'
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_numeric_question_with_null_text():
    form_id = get_mock_form()
    question_text = None
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_numeric_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = None
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400
    
@pytest.mark.django_db
def test_post_numeric_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 'Try again'
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_numeric_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = None
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_numeric_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = None
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_numeric_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    data = {
        'type': 'numeric',
        'form_id': form_id,
        'text': question_text,
        'ordinal': ordinal,
        'explainer': explainer,
        'is_mandatory': is_mandatory,
        'is_integer': is_integer,
        'min_value': min_value,
        'max_value': max_value
    }
    request_url = url + str(form_id) + '/questions/'
    print(request_url)
    response = client.post(request_url, data, format='json')
    assert response.status_code == 200
    id = response.data['id']
    assert id is not None
    question = NumericQuestion.objects.get(pk=id)
    assert question.text == question_text
    assert question.ordinal == ordinal
    assert question.explainer == explainer
    assert question.is_mandatory == is_mandatory

# Test updates to numeric questions
@pytest.mark.django_db
def test_put_numeric_question_with_null_data():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = None
    new_ordinal = None
    new_explainer = None
    new_is_mandatory = None
    new_is_integer = None
    new_min_val = None
    new_max_val = None

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_numeric_question_with_null_text():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = None
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_numeric_question_with_null_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = None
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_numeric_question_with_non_numeric_ordinal():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 'Hmmm'
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_numeric_question_with_null_explainer():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = None
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_numeric_question_with_null_is_mandatory():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = None
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_put_numeric_question():
    form_id = get_mock_form()
    question_text = 'How do you like your eggs in the morning?'
    ordinal = 1
    explainer = 'A very serious tax-related question'
    is_mandatory = True
    is_integer = False
    min_value = 0
    max_value = 100

    id = create_numeric_question(form_id, question_text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value)

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 200

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
def test_put_numeric_question_with_non_existent_id():
    form_id = get_mock_form()
    question_id = 5196

    new_text = 'Please describe how you like your eggs in the morning.'
    new_ordinal = 2
    new_explainer = 'Boiled or fried and whether or not you are satisfied by eggs alone.'
    new_is_mandatory = False
    new_is_integer = True
    new_min_val = -10
    new_max_val = 10

    data = {
        'type': 'numeric',
        'text': new_text,
        'ordinal': new_ordinal,
        'explainer': new_explainer,
        'is_mandatory': new_is_mandatory,
        'is_integer': new_is_integer,
        'min_value': new_min_val,
        'max_value': new_max_val
    }
    request_url = url + str(form_id) + '/questions/' + str(id) + '/'
    print(request_url)
    response = client.put(request_url, data, format='json')
    assert response.status_code == 404

# Test deleting questions
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
        False
    )
    assert Form.objects.all().count() == 1
    request_url = url + str(id) + '/'
    response = client.delete(request_url)
    assert response.status_code == 200
    assert Form.objects.all().count() == 0

@pytest.mark.django_db
def test_delete_question_with_non_existent_id():
    id = 1561651
    request_url = url + str(id) + '/'
    response = client.delete(request_url)
    assert response.status_code == 404

# Test creation of multiple choice options
# Helper
def get_mock_multiple_choice_question(form_id):
    return create_multiple_choice_question(form_id, 'Wibble', 1, 'Wobble', True)

@pytest.mark.django_db
def test_post_option_with_null_text():
    form_id = get_mock_form()
    question_id = get_mock_multiple_choice_question(form_id)
    request_url = url + str(form_id) + '/questions/' + str(question_id) + '/options'

    text = None
    data = {
        'question_id': question_id,
        'text': text
    }
    response = client.post(request_url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_option():
    form_id = get_mock_form()
    question_id = get_mock_multiple_choice_question(form_id)
    request_url = url + str(form_id) + '/questions/' + str(question_id) + '/options'

    text = 'My question'
    data = {
        'question_id': question_id,
        'text': text
    }
    response = client.post(request_url, data, format='json')
    assert response.status_code == 200
    assert id is not None
    option = MultipleChoiceOption.objects.get(pk=id)
    assert option.text == text

# Test deletion of multiple choice options
def get_mock_option(question_id):
    return create_multiple_choice_option(question_id, option)

@pytest.mark.django_db
def test_delete_option():
    assert MultipleChoiceOption.objects.all().count() == 0
    text = 'Boiled'
    form_id = get_mock_form()
    question_id = get_mock_multiple_choice_question(form_id)
    id = create_multiple_choice_option(quetion_id, text)
    option = MultipleChoiceOption.objects.get(pk=id)
    assert option.text == text
    assert MultipleChoiceOption.objects.all().count() == 1
    request_url = url + str(form_id) + '/questions/' + str(question_id) + '/options' + str(id) + '/'
    response = client.delete(request_url)
    assert response.status_code == 200
    assert MultipleChoiceOption.objects.all().count() == 0

@pytest.mark.django_db
def test_delete_option_with_non_existent_id():
    form_id = get_mock_form()
    question_id = get_mock_multiple_choice_question(form_id)
    option_id = 1561561
    request_url = url + str(form_id) + '/questions/' + str(question_id) + '/options' + str(option_id) + '/'
    response = client.delete(request_url)
    assert response.status_code == 400

        