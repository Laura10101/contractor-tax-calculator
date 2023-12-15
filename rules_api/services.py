from .models import *
from django.core.exceptions import ValidationError

### RULE SETS ###
# Create rule set
def create_ruleset(jurisdiction_id, tax_category_id, ordinal):
    if not isinstance(jurisdiction_id, int) or jurisdiction_id < 0:
        raise ValidationError('jurisdiction_id must be a valid (non-negative, non-null) integer')
    
    if RuleSet.objects.filter(jurisdiction_id__exact=jurisdiction_id, tax_category_id__exact=tax_category_id).count() > 0:
        raise ValidationError('A rule already exists with for this tax category in this jurisdiction')
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
    ruleset = RuleSet.objects.get(pk=id)
    ruleset.delete()

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
    tax_category = TaxCategory.objects.get(pk=id)
    tax_category.delete()

### GENERIC RULES ###
def delete_rule(id):
    rule = Rule.objects.get(pk=id)
    rule.delete()

### FLAT RATE RULES ###
# Create rule 
def create_flat_rate_rule(ruleset_id, name, ordinal, explainer, variable_name, tax_rate):
    if not isinstance(ruleset_id, int) or ruleset_id < 0:
        raise RuleSet.DoesNotExist('ruleset_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
    if not isinstance(tax_rate, float) and not isinstance(tax_rate, int):
        raise ValidationError('tax_rate must be a non-negative floating point value')

    ruleset = RuleSet.objects.get(pk=ruleset_id)

    flat_rate_rule = FlatRateRule()
    flat_rate_rule.ruleset = ruleset
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
    if not isinstance(id, int) or id < 0:
        raise FlatRateRule.DoesNotExist('rule_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
    if not isinstance(tax_rate, float) and not isinstance(tax_rate, int):
        raise ValidationError('tax_rate must be a non-negative integer value')
    
    rule = FlatRateRule.objects.get(pk=id)
    rule.name=name
    rule.ordinal=ordinal
    rule.explainer=explainer
    rule.variable_name=variable_name
    rule.flat_rate=tax_rate
    rule.full_clean()
    rule.save()

### TIERED RATE RULES ###
def create_tiered_rate_rule(ruleset_id, name, ordinal, explainer, variable_name):
    if not isinstance(ruleset_id, int) or ruleset_id < 0:
        raise RuleSet.DoesNotExist('ruleset_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
    ruleset = RuleSet.objects.get(pk=ruleset_id)
    
    tiered_rate_rule = TieredRateRule()
    tiered_rate_rule.ruleset=ruleset
    tiered_rate_rule.name=name
    tiered_rate_rule.ordinal=ordinal
    tiered_rate_rule.explainer=explainer
    tiered_rate_rule.variable_name=variable_name
    tiered_rate_rule.full_clean()
    tiered_rate_rule.save()
    return tiered_rate_rule.id

def update_tiered_rate_rule(id, name, ordinal, explainer, variable_name):
    if not isinstance(id, int) or id < 0:
        raise TieredRateRule.DoesNotExist('rule_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
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
    if not isinstance(rule_id, int) or id < 0:
        raise TieredRateRule.DoesNotExist('rule_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
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
    if not isinstance(id, int) or id < 0:
        raise RuleTier.DoesNotExist('tier_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
    rule_tier = RuleTier.objects.get(pk=id)
    rule_tier.min_value=min_value
    rule_tier.max_value=max_value
    rule_tier.ordinal=ordinal
    rule_tier.tier_rate=tier_rate
    rule_tier.full_clean()
    rule_tier.save()
    
def delete_rule_tier(id):
    tier = RuleTier.objects.get(pk=id)
    tier.delete()

### SECONDARY TIERED RATE RULES ###
def create_secondary_tiered_rate_rule(ruleset_id, primary_rule_id, name, ordinal, explainer, variable_name):
    if not isinstance(ruleset_id, int) or ruleset_id < 0:
        raise RuleSet.DoesNotExist('ruleset_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
    ruleset = RuleSet.objects.get(pk=ruleset_id)

    primary_rule = TieredRateRule.objects.get(pk=primary_rule_id)
    secondary_tiered_rate_rule = SecondaryTieredRateRule()
    secondary_tiered_rate_rule.ruleset=ruleset
    secondary_tiered_rate_rule.primary_rule = primary_rule
    secondary_tiered_rate_rule.name=name
    secondary_tiered_rate_rule.ordinal=ordinal
    secondary_tiered_rate_rule.explainer=explainer
    secondary_tiered_rate_rule.variable_name=variable_name
    secondary_tiered_rate_rule.full_clean()
    secondary_tiered_rate_rule.save()
    return secondary_tiered_rate_rule.id

def update_secondary_tiered_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate):
    if not isinstance(id, int) or id < 0:
        raise FlatRateRule.DoesNotExist('rule_id must be a non-negative integer value')
    
    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')
    
    secondary_tiered_rate_rule = SecondaryTieredRateRule.objects.get(pk=id)
    secondary_tiered_rate_rule.name=name
    secondary_tiered_rate_rule.ordinal=ordinal
    secondary_tiered_rate_rule.explainer=explainer
    secondary_tiered_rate_rule.variable_name=variable_name
    secondary_tiered_rate_rule.full_clean()
    secondary_tiered_rate_rule.save()

### SECONDARY RULE TIER ###
def create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate):
    if not isinstance(secondary_rule_id, int) or id < 0:
        raise SecondaryTieredRateRule.DoesNotExist('rule_id must be a non-negative integer value')
    
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
    if not isinstance(id, int) or id < 0:
        raise SecondaryRuleTier.DoesNotExist('tier_id must be a non-negative integer value')
    
    secondary_rule_tier = SecondaryRuleTier.objects.get(pk=id)
    secondary_rule_tier.tier_rate=tier_rate
    secondary_rule_tier.full_clean()
    secondary_rule_tier.save()

def delete_secondary_rule_tier(id):
    tier = SecondaryRuleTier.objects.get(pk=id)
    tier.delete()

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