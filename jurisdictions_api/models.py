from django.db import models

# Create your models here.
class Jurisdiction(models.Model):
    # No need to create ID attribute as Django will create automatically
    # Info taken from Tim Nelson Models: Part 1 CI video at 5.30.

    # Add name attribute and validation rules for attribute
    name = models.CharField(max_length=50, null=False, blank=False)