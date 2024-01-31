from django.contrib import admin
from .models import TaxCategory, RuleSet, FlatRateRule, TieredRateRule, SecondaryTieredRateRule, \
    RuleTier, SecondaryRuleTier

from .forms import RuleSetForm

class RuleSetAdmin(admin.ModelAdmin):
    form = RuleSetForm

# Register your models here.
admin.site.register(TaxCategory)