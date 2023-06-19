from django.contrib import admin
from .models import TaxCategory, RuleSet, FlatRateRule, TieredRateRule, SecondaryTieredRateRule, \
    RuleTier, SecondaryRuleTier

from .forms import RuleSetForm

class RuleSetAdmin(admin.ModelAdmin):
    form = RuleSetForm

# Register your models here.
admin.site.register(TaxCategory)
admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(FlatRateRule)
admin.site.register(TieredRateRule)
admin.site.register(SecondaryTieredRateRule)
admin.site.register(RuleTier)
admin.site.register(SecondaryRuleTier)