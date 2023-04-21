from .models import *

# Create new method to get forms by jurisidiction ids 
def get_forms_by_jurisdiction_ids(jurisdiction_ids):
    forms = Form.objects.filter(jursidiction_id__in=jurisdiction_ids)
    return forms

# Create new method to create forms 
def create_form(jurisdiction_id):
    # Create new form in the database
    new_form = Form.objects.create(jurisdiction_id=jurisdiction_id)
    # Return ID of newly created form
    return new_form.id

# Create new method to delete forms 
def delete_forms(id): 
    Form.objects.filter(pk__exact=id).delete()    

# Create new method to create questions 
# Requires 3 methods - one for each type of question

def create_boolean_question(form_id, text, ordinal, explainer, is_mandatory):
    # Get form object by its primary key 
    form = Form.objects.filter(pk__exact=form_id)
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

def create_multiple_choice_question(form_id, text, ordinal, explainer, is_mandatory):
    # Get form object by its primary key 
    form = Form.objects.filter(pk__exact=form_id)
    # Create new question in the database
    new_question = MultipleChoiceQuestion.objects.create(
        form=form,
        text=text,
        ordinal=ordinal,
        explainer=explainer,
        is_mandatory=is_mandatory
        )
    # Return ID of newly created question
    return new_question.id
    
def create_numeric_question(form_id, text, ordinal, explainer, is_mandatory, is_integer, min_value, max_value):
    # Get form object by its primary key 
    form = Form.objects.filter(pk__exact=form_id)
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
def update_question():
    pass

# Create new method to delete questions
def delete_question(id):
    Question.objects.filter(pk__exact=id).delete()
