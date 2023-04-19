from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.
class Form(models.Model):
    pass

class Question(PolymorphicModel):
    pass

class BooleanQuestion(Question):
    pass

class MultipleChoiceQuestion(Question):
    pass

class MultipleChoiceOption(models.Model):
    pass

class NumericQuestion(Question):
    pass

class NumericAnswerValidationRule(models.Model):
    pass