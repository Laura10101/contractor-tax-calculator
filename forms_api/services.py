from .models import *
from django.core.exceptions import ValidationError

# Create new method to get forms by jurisidiction ids 
def get_forms_by_jurisdiction_ids(jurisdiction_ids):
    if not isinstance(jurisdiction_ids, list) or len(jurisdiction_ids) == 0:
        raise ValidationError('A valid list of numeric jurisdiction_ids must be specified')

    for jurisdiction_id in jurisdiction_ids:
        if not isinstance(jurisdiction_id, int):
            raise ValidationError('Only valid integers may be included in the list of jurisdiction_ids')

    forms = Form.objects.filter(jurisdiction_id__in=jurisdiction_ids)
    return forms

# Create new method to create forms 
def create_form(jurisdiction_id):
    # Create new form in the database
    new_form = Form()
    new_form.jurisdiction_id = jurisdiction_id
    new_form.full_clean()
    new_form.save()
    # Return ID of newly created form
    return new_form.id

# Create new method to delete forms 
def delete_form(id): 
    Form.objects.get(pk=id).delete()    

# Create new method to create questions 
# Requires 3 methods - one for each type of question

def create_boolean_question(form_id, text, ordinal, explainer, is_mandatory):
    if form_id is None or not isinstance(form_id, int):
        raise ValidationError('The form_id must be a valid integer when creating a question')
    # Get form object by its primary key 
    form = Form.objects.get(pk=form_id)
    # Create new question in the database
    new_question = BooleanQuestion()
    new_question.form=form
    new_question.text=text
    new_question.ordinal=ordinal
    new_question.explainer=explainer
    new_question.is_mandatory=is_mandatory
    new_question.full_clean()
    new_question.save()
    # Return ID of newly created question
    return new_question.id

def create_multiple_choice_question(form_id, text, ordinal, explainer, is_mandatory, is_multiselect=False):
    if form_id is None or not isinstance(form_id, int):
        raise ValidationError('The form_id must be a valid integer when creating a question')
    # Get form object by its primary key 
    form = Form.objects.get(pk=form_id)
    # Create new question in the database
    new_question = MultipleChoiceQuestion()
    new_question.form=form
    new_question.text=text
    new_question.ordinal=ordinal
    new_question.explainer=explainer
    new_question.is_mandatory=is_mandatory
    new_question.is_multiselect=is_multiselect
    new_question.full_clean()
    new_question.save()

    # Return ID of newly created question
    return new_question.id
    
def create_numeric_question(form_id, text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value):
    if form_id is None or not isinstance(form_id, int):
        raise ValidationError('The form_id must be a valid integer when creating a question')
    # Get form object by its primary key 
    form = Form.objects.get(pk=form_id)

    # Create new question in the database
    new_question = NumericQuestion()
    new_question.form=form
    new_question.text=text
    new_question.ordinal=ordinal
    new_question.explainer=explainer
    new_question.is_mandatory=is_mandatory
    new_question.is_integer=is_integer
    new_question.min_value=min_value
    new_question.max_value=max_value
    new_question.full_clean()
    new_question.save()
    # Return ID of newly created question
    return new_question.id

# Create new method to update questions 
def update_boolean_question(id, text, ordinal, explainer, is_mandatory):
    question = BooleanQuestion.objects.get(pk=id)
    question.text=text
    question.ordinal=ordinal
    question.explainer=explainer
    question.is_mandatory=is_mandatory
    question.full_clean()
    question.save()

def update_multiple_choice_question(id, text, ordinal, explainer, is_mandatory, is_multiselect=False):
    question = MultipleChoiceQuestion.objects.get(pk=id)
    question.text=text
    question.ordinal=ordinal
    question.explainer=explainer
    question.is_mandatory=is_mandatory
    question.is_multiselect=is_multiselect
    question.full_clean()
    question.save()

def update_numeric_question(id, text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value):
    # Here I am updating two objects rather than one as the int/val fields are from the validation rule 
    # class
    # First, update the question data
    # Create a variable to store the updated question info
    question = NumericQuestion.objects.get(pk=id)
    # Perform the update on the question
    question.text=text
    question.ordinal=ordinal
    question.explainer=explainer
    question.is_mandatory=is_mandatory
    question.is_integer=is_integer
    question.min_value=min_value
    question.max_value=max_value
    question.full_clean()
    question.save()

# Create new method to delete questions
def delete_question(id):
    Question.objects.get(pk=id).delete()

# Services to add and remove multiple choice options
def create_multiple_choice_option(question_id, text, explainer):
    if question_id is None or not isinstance(question_id, int):
        raise ValidationError('The question_id must be a valid integer when creating a multiple choice option')

    question = Question.objects.get(pk=question_id)

    option = MultipleChoiceOption()
    option.question = question
    option.text = text
    option.explainer = explainer
    option.full_clean()
    option.save()

def delete_multiple_choice_option(id):
    MultipleChoiceOption.objects.get(pk=id).delete()