from django.db import models
from polymorphic.models import PolymorphicModel

from jurisdictions_api.models import Jurisdiction

# Create your models here.
class Form(models.Model):
    # Questions - one to many so the code for this is in the Question class as that is where
    # the foreign key needs to be
    # Jurisdiction ID 
    jurisdiction_id = models.IntegerField()

    def __str__(self):
        return Jurisdiction.objects.get(pk=self.jurisdiction_id).name + '  Form'

class Question(PolymorphicModel):
    # Create foreign key for Form/Question relationship 
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    # Question text 
    text = models.CharField(max_length=255, null=False, blank=False)
    # ordinal to indicate order in which questions are asked 
    ordinal = models.IntegerField()
    # Explanatory text box 
    explainer = models.CharField(max_length=255, null=False, blank=False)
    # Is question mandatory or not
    is_mandatory = models.BooleanField()

    def __str__(self):
        return str(self.form) + ': ' + text

class BooleanQuestion(Question):
    pass
    # Nothing extra needed here 

class MultipleChoiceQuestion(Question):
    # Possible multiple choices - one to many 
    # The code for this is in MultipleChoiceOption as that is where the 
    # foreign key needs to be

    # Whether multiselect or single select 
    is_multiselect = models.BooleanField()

class MultipleChoiceOption(models.Model):
    # Create foreign key for MultipleChoiceQuestion/MCOption 
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    # Option text 
    text = models.CharField(max_length=255, null=False, blank=False)
    # Explanatory notes for each option 
    explainer = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.question) + ' - ' + self.text

class NumericQuestion(Question):
    # Is integer: boolean
    is_integer = models.BooleanField(default=False)
    # Min value 
    min_value = models.IntegerField()
    # Max value
    max_value = models.IntegerField(null=True, blank=True)
