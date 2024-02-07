"""Models for the forms API."""

from django.db import models
from polymorphic.models import PolymorphicModel

from jurisdictions_api.models import Jurisdiction


class Form(models.Model):
    """Form model."""
    """Groups the questions associated with a specific jurisdiction."""
    # Questions - one to many so the code for this is in the
    # Question class as that is where the foreign key needs to be
    # Jurisdiction ID
    jurisdiction_id = models.IntegerField(unique=True)

    def __str__(self):
        return Jurisdiction.objects.get(
            pk=self.jurisdiction_id
        ).name + '  Form'


class Question(PolymorphicModel):
    """Question model."""
    """Parent class for all concrete question models."""
    """Defines the base data needed for all question types."""
    # Create foreign key for Form/Question relationship
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='questions',
        null=False,
        blank=False
    )
    # Question text
    text = models.CharField(max_length=255, null=False, blank=False)
    # ordinal to indicate order in which questions are asked
    ordinal = models.IntegerField()
    # Explanatory text box
    explainer = models.CharField(max_length=255, null=False, blank=False)
    # Is question mandatory or not
    is_mandatory = models.BooleanField(default=False)
    # The machine-friendly name that will be used by rules to
    # reference the answer to this question
    variable_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return str(self.form) + ': ' + self.text


class BooleanQuestion(Question):
    """Define the boolean question model."""
    """A boolean question has a yes/no answer."""

    # No additional attributes needed for a boolean question
    pass


class MultipleChoiceQuestion(Question):
    """Define the multiple choice question model."""
    """A multiple choice question requires a user to select"""
    """from a number of options defined by the admin."""

    # Possible multiple choices - one to many
    # The code for this is in MultipleChoiceOption as that is where the
    # foreign key needs to be

    # Whether multiselect or single select
    is_multiselect = models.BooleanField()


class MultipleChoiceOption(models.Model):
    """Define the multiple choice option model."""
    """A multiple choice option is one of a number of options"""
    """which a user can select for a multiple choice question."""

    # Create foreign key for MultipleChoiceQuestion/MCOption
    question = models.ForeignKey(
        MultipleChoiceQuestion,
        on_delete=models.CASCADE,
        related_name='options'
    )
    # Option text
    text = models.CharField(max_length=255, null=False, blank=False)
    # Explanatory notes for each option
    explainer = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.question) + ' - ' + self.text


class NumericQuestion(Question):
    """Define the numeric question model."""
    """A numeric question requires a numeric response"""
    """within the min/max values and integer/float constraint"""
    """defined by the admin."""

    # Is integer: boolean
    is_integer = models.BooleanField(default=False)
    # Min value
    min_value = models.IntegerField()
    # Max value
    max_value = models.IntegerField(null=True, blank=True)
