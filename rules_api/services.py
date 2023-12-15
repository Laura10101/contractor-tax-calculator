from .models import *
from django.core.exceptions import ValidationError

### RULE SETS ###
# Create rule set
def create_ruleset(jurisdiction_id, tax_category_id, ordinal):
    if not isinstance(jurisdiction_id, int) or jurisdiction_id < 0:
        raise ValidationError('jurisdiction_id must be a valid (non-negative, non-null) integer')
    # Assign tax category id to new rule set 
    tax_category = TaxCategory.objects.get(pk=tax_category_id)
    # Create new ruleset in the database
    new_ruleset = RuleSet()
    new_ruleset.jurisdiction_id=jurisdiction_id
    new_ruleset.tax_category=tax_category
    new_ruleset.ordinal=ordinal
    new_ruleset.full_clean()
    new_ruleset.save()
    # Return ID of newly created ruleset
    return new_ruleset.id

# Delete rule set 
def delete_ruleset(id):
    RuleSet.objects.filter(pk__exact=id).delete()

### TAX CATEGORIES ###
# Create tax category
def create_tax_category(name):
    tax_category = TaxCategory()
    tax_category.name=name
    tax_category.full_clean()
    tax_category.save()
    return tax_category.id

# Delete tax category
def delete_tax_category(id):
    TaxCategory.objects.filter(pk__exact=id).delete()

### GENERIC RULES ###
def delete_rule(id):
    Rule.objects.filter(pk__exact=id).delete()

### FLAT RATE RULES ###
# Create rule 
def create_flat_rate_rule(name, ordinal, explainer, variable_name, tax_rate):
    flat_rate_rule = FlatRateRule()
    flat_rate_rule.name=name
    flat_rate_rule.ordinal=ordinal
    flat_rate_rule.explainer=explainer
    flat_rate_rule.variable_name=variable_name
    flat_rate_rule.flat_rate=tax_rate
    flat_rate_rule.full_clean()
    flat_rate_rule.save()
    return flat_rate_rule.id

# Update rule 
def update_flat_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate):
    rule = FlatRateRule.objects.get(pk=id)
    rule.name=name
    rule.ordinal=ordinal
    rule.explainer=explainer
    rule.variable_name=variable_name
    rule.flat_rate=tax_rate
    rule.full_clean()
    rule.save()

### TIERED RATE RULES ###
def create_tiered_rate_rule(name, ordinal, explainer, variable_name):
    tiered_rate_rule = TieredRateRule()
    tiered_rate_rule.name=name
    tiered_rate_rule.ordinal=ordinal
    tiered_rate_rule.explainer=explainer
    tiered_rate_rule.variable_name=variable_name
    tiered_rate_rule.full_clean()
    tiered_rate_rule.save()
    return tiered_rate_rule.id

def update_tiered_rate_rule(id, name, ordinal, explainer, variable_name):
    tiered_rate_rule = TieredRateRule.objects.get(pk=id)
    tiered_rate_rule.name=name
    tiered_rate_rule.ordinal=ordinal
    tiered_rate_rule.explainer=explainer
    tiered_rate_rule.variable_name=variable_name
    tiered_rate_rule.full_clean()
    tiered_rate_rule.save()

### RULE TIER ###
# create a method to create rule tier
def create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate):
    # Get the rule from the database based on the rule id
    rule = Rule.objects.get(pk=rule_id)
    rule_tier = RuleTier()
    rule_tier.rule=rule
    rule_tier.min_value=min_value
    rule_tier.max_value=max_value
    rule_tier.ordinal=ordinal
    rule_tier.tier_rate=tier_rate
    rule_tier.full_clean()
    rule_tier.save()
    return rule_tier.id

def update_rule_tier(id, min_value, max_value, ordinal, tier_rate):
    rule_tier = RuleTier.objects.get(pk=id)
    rule_tier.min_value=min_value
    rule_tier.max_value=max_value
    rule_tier.ordinal=ordinal
    rule_tier.tier_rate=tier_rate
    rule_tier.full_clean()
    rule_tier.save()
    
def delete_rule_tier(id):
    RuleTier.objects.filter(pk__exact=id).delete()

### SECONDARY TIERED RATE RULES ###
def create_secondary_tiered_rate_rule(primary_rule_id, name, ordinal, explainer, variable_name):
    primary_rule = TieredRateRule.objects.get(pk=primary_rule_id)
    secondary_tiered_rate_rule = SecondaryTieredRateRule()
    secondary_tiered_rate_rule.primary_rule = primary_rule
    secondary_tiered_rate_rule.name=name
    secondary_tiered_rate_rule.ordinal=ordinal
    secondary_tiered_rate_rule.explainer=explainer
    secondary_tiered_rate_rule.variable_name=variable_name
    secondary_tiered_rate_rule.full_clean()
    secondary_tiered_rate_rule.save()
    return secondary_tiered_rate_rule.id

def update_secondary_tiered_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate):
    secondary_tiered_rate_rule = SecondaryTieredRateRule.objects.get(pk=id)
    secondary_tiered_rate_rule.name=name
    secondary_tiered_rate_rule.ordinal=ordinal
    secondary_tiered_rate_rule.explainer=explainer
    secondary_tiered_rate_rule.variable_name=variable_name
    secondary_tiered_rate_rule.full_clean()
    secondary_tiered_rate_rule.save()

### SECONDARY RULE TIER ###
def create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate):
    # Get the primary rule object from the database based on the rule tier id
    secondary_rule = SecondaryTieredRateRule.objects.get(pk=secondary_rule_id)
    primary_tier = RuleTier.objects.get(pk=primary_tier_id)
    secondary_rule_tier = SecondaryRuleTier()
    secondary_rule_tier.secondary_rule=secondary_rule
    secondary_rule_tier.primary_tier=primary_tier
    secondary_rule_tier.tier_rate=tier_rate
    secondary_rule_tier.full_clean()
    secondary_rule_tier.save()
    return secondary_rule_tier.id

def update_secondary_rule_tier(id, tier_rate):
    secondary_rule_tier = SecondaryRuleTier.objects.get(pk=id)
    secondary_rule_tier.tier_rate=tier_rate
    secondary_rule_tier.full_clean()
    secondary_rule_tier.save()

def delete_secondary_rule_tier(id):
    SecondaryRuleTier.objects.filter(pk__exact=id).delete()

# Calculations
def create_calculation(username, jurisdiction_ids, variable_table):
    calculation_result = TaxCalculationResult()
    calculation_result.username=username
    calculation_result.full_clean()
    calculation_result.save()
    
    for jurisdiction_id in jurisdiction_ids:
        rulesets = RuleSet.objects.filter(jurisdiction_id__exact=jurisdiction_id).order_by('ordinal')
        for ruleset in rulesets:
            ruleset.calculate(variable_table, calculation_result)

    return calculation_result

def get_calculations_for_user(username):
    return TaxCalculationResult.objects.filter(username__exact=username).order_by('-created')