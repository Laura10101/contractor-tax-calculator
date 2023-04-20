from .models import *

# Create new method to get forms by jurisidiction ids 
def get_forms_by_jurisdiction_ids(jurisdiction_ids):
    forms = Form.objects.filter(jursidiction_id__in=jurisdiction_ids)
    return forms

# Create new method to create forms 
def create_form():
    pass

# Create new method to update forms 
def update_forms():
    pass

# Create new method to delete forms 
def delete_forms(): 
    pass 

# Create new method to create questions 
def create_question():
    pass

# Create new method to update questions 
def update_question():
    pass

# Create new method to delete questions
def delete_question():
    pass 
