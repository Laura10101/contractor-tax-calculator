from .models import *

# Create new method to get forms by jurisidiction ids 
def get_forms_by_jurisdiction_ids(jurisdiction_ids):
    forms = Form.objects.filter(jursidiction_id__in=jurisdiction_ids)
    return forms

# Create new method to create forms 
def create_form():
    pass

# Create new method to delete forms 
def delete_forms(id): 
    Form.objects.filter(pk__exact=id).delete()
    

# Create new method to create questions 
def create_question():
    pass

# Create new method to update questions 
def update_question():
    pass

# Create new method to delete questions
def delete_question(id):
    Question.objects.filter(pk__exact=id).delete()
