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
    # Get form object by its primary key 
    form = Form.objects.get(pk=form_id)
    # Create new question in the database
    new_question = BooleanQuestion.objects.create(
        form=form,
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory
        )
    # Return ID of newly created question
    return new_question.id

def create_multiple_choice_question(form_id, text, ordinal, explainer, is_mandatory, is_multiselect=False):
    # Get form object by its primary key 
    form = Form.objects.get(pk=form_id)
    # Create new question in the database
    new_question = MultipleChoiceQuestion.objects.create(
        form=form,
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory,
        is_multiselect=is_multiselect
        )
    # Return ID of newly created question
    return new_question.id
    
def create_numeric_question(form_id, text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value):
    # Get form object by its primary key 
    form = Form.objects.get(pk=form_id)
    print("Form is: " + str(form))
    # Create numeric validation rule for this question 
    validation_rule = NumericAnswerValidationRule.objects.create(
        is_integer=is_integer,
        min_value=min_value,
        max_value=max_value
    )

    # Create new question in the database
    new_question = NumericQuestion.objects.create(
        form=form,
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory,
        validation_rule=validation_rule
        )
    # Return ID of newly created question
    return new_question.id

# Create new method to update questions 
def update_boolean_question(id, text, ordinal, explainer, is_mandatory):
    BooleanQuestion.objects.get(pk=id).update(
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory
        )

def update_multiple_choice_question(id, text, ordinal, explainer, is_mandatory, is_multiselect=False):
    MultipleChoiceQuestion.objects.get(pk=id).update(
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory,
        is_multiselect=is_multiselect
    )

def update_numeric_question(id, text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value):
    # Here I am updating two objects rather than one as the int/val fields are from the validation rule 
    # class
    # First, update the question data
    # Create a variable to store the updated question info
    question = NumericQuestion.objects.get(pk=id)
    # Perform the update on the question
    question.update(
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory
    )
    # Second, perform the update on the validation rule
    question.validation_rule.update(
        is_integer=is_integer,
        min_value=min_value, 
        max_value=max_value
    )

# Create new method to delete questions
def delete_question(id):
    Question.objects.get(pk=id).delete()
