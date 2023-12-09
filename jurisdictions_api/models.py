from django.db import models
from django.core import validators

# Create your models here.
class Jurisdiction(models.Model):
    # No need to create ID attribute as Django will create automatically
    # Info taken from Tim Nelson Models: Part 1 CI video at 5.30.

    # Add name attribute and validation rules for attribute
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, validators=[validators.MinLengthValidator(3)])

    def __str__(self):
        return self.name