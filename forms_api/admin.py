from django.contrib import admin
from .models import Form, BooleanQuestion, MultipleChoiceQuestion, MultipleChoiceOption, NumericQuestion

from .forms import FormForm

class FormAdmin(admin.ModelAdmin):
    form = FormForm

admin.site.register(Form, FormAdmin)
admin.site.register(BooleanQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceOption)
admin.site.register(NumericQuestion)