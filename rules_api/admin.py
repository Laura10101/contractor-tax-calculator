from django.contrib import admin
from .models import TaxCategory, RuleSet, FlatRateRule, TieredRateRule, SecondaryTieredRateRule, \
    RuleTier, SecondaryRuleTier

# Register your models here.
admin.site.register(TaxCategory)
admin.site.register(RuleSet)
admin.site.register(FlatRateRule)
admin.site.register(TieredRateRule)
admin.site.register(SecondaryTieredRateRule)
admin.site.register(RuleTier)
admin.site.register(SecondaryRuleTier)