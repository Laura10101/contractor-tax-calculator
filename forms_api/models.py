from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.
class Form(models.Model):
    pass
    # Questions - one to many 
    
    # Jurisdiction ID 
    jurisdiction_id = models.IntegerField()

class Question(PolymorphicModel):
    # Question text 
    text = models.CharField(max_length=255, null=False, blank=False)
    # ordinal to indicate order in which questions are asked 
    ordinal = models.IntegerField()
    # Explanatory text box 
    explainer = models.CharField(max_length=255, null=False, blank=False)
    # Is question mandatory or not
    is_mandatory = models.BooleanField()

class BooleanQuestion(Question):
    pass
    # Nothing extra needed here 

class MultipleChoiceQuestion(Question):
    pass
    # Possible multiple choices - one to many 
    # Whether multiselect or single select 
    is_multiselect = models.BooleanField()

class MultipleChoiceOption(models.Model):
    # Option text 
    text = models.CharField(max_length=255, null=False, blank=False)
    # Explanatory notes for each option 
    explainer = models.CharField(max_length=255, null=False, blank=False)

class NumericQuestion(Question):
    pass
    # Numeric validation rule - one to one 

class NumericAnswerValidationRule(models.Model):
    # Is integer: boolean
    is_integer = models.BooleanField()
    # Min value 
    min_value = models.IntegerField()
    # Max value
    max_value = models.IntegerField()
