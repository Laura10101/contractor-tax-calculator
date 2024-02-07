"""Add the form model to the admin app."""

from django.contrib import admin
from .models import (
    Form,
    BooleanQuestion,
    MultipleChoiceQuestion,
    MultipleChoiceOption,
    NumericQuestion
)

from .forms import FormForm


class FormAdmin(admin.ModelAdmin):
    """Admin configuration for the form model"""

    form = FormForm


admin.site.register(Form, FormAdmin)
