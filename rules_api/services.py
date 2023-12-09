from .models import *

### RULE SETS ###
# Create rule set
def create_ruleset(jurisdiction_id, tax_category_id):
    # Assign tax category id to new rule set 
    tax_category = TaxCategory.objects.get(pk=tax_category_id)
    # Create new ruleset in the database
    new_ruleset = RuleSet.objects.create(
        jurisdiction_id=jurisdiction_id,
        tax_category=tax_category
        )
    # Return ID of newly created ruleset
    return new_ruleset.id

# Delete rule set 
def delete_ruleset(id):
    RuleSet.objects.filter(pk__exact=id).delete()

### TAX CATEGORIES ###
# Create tax category
def create_tax_category(name):
    tax_category = TaxCategory.objects.create(name=name)
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
    flat_rate_rule = FlatRateRule.objects.create(
        name=name, 
        ordinal=ordinal, 
        explainer=explainer, 
        variable_name=variable_name,
        flat_rate=tax_rate
        )
    return flat_rate_rule.id

# Update rule 
def update_flat_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate):
    FlatRateRule.objects.filter(pk__exact=id).update(
        name=name,
        ordinal=ordinal,
        explainer=explainer,
        variable_name=variable_name,
        flat_rate=tax_rate        
        )

### TIERED RATE RULES ###
def create_tiered_rate_rule(name, ordinal, explainer, variable_name):
    tiered_rate_rule = TieredRateRule.objects.create(
        name=name, 
        ordinal=ordinal, 
        explainer=explainer, 
        variable_name=variable_name
        )
    return tiered_rate_rule.id

def update_tiered_rate_rule(id, name, ordinal, explainer, variable_name):
    TieredRateRule.objects.filter(pk__exact=id).update(
        name=name,
        ordinal=ordinal,
        explainer=explainer,
        variable_name=variable_name       
        )

### RULE TIER ###
# create a method to create rule tier
def create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate):
    # Get the rule from the database based on the rule id
    rule = Rule.objects.get(pk=rule_id)
    rule_tier = RuleTier.objects.create(
        rule=rule,
        min_value=min_value,
        max_value=max_value,
        ordinal=ordinal,
        tier_rate=tier_rate
    )
    return rule_tier.id

def update_rule_tier(id, min_value, max_value, ordinal, tier_rate):
    RuleTier.objects.filter(pk__exact=id).update(
        min_value=min_value,
        max_value=max_value,
        ordinal=ordinal,
        tier_rate=tier_rate   
        )
    
def delete_rule_tier(id):
    RuleTier.objects.filter(pk__exact=id).delete()

### SECONDARY TIERED RATE RULES ###
def create_secondary_tiered_rate_rule(primary_rule_id, name, ordinal, explainer, variable_name):
    primary_rule = TieredRateRule.objects.get(pk=primary_rule_id)
    secondary_tiered_rate_rule = SecondaryTieredRateRule.objects.create(
        primary_rule = primary_rule,
        name=name, 
        ordinal=ordinal, 
        explainer=explainer, 
        variable_name=variable_name
        )
    return secondary_tiered_rate_rule.id

def update_secondary_tiered_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate):
    SecondaryTieredRateRule.objects.filter(pk__exact=id).update(
        name=name, 
        ordinal=ordinal, 
        explainer=explainer, 
        variable_name=variable_name   
        )

### SECONDARY RULE TIER ###
def create_secondary_rule_tier(secondary_rule_id, primary_tier_id, tier_rate):
    # Get the primary rule object from the database based on the rule tier id
    secondary_rule = SecondaryTieredRateRule.objects.get(pk=secondary_rule_id)
    primary_tier = RuleTier.objects.get(pk=primary_tier_id)
    secondary_rule_tier = SecondaryRuleTier.objects.create(
        secondary_rule=secondary_rule,
        primary_tier=primary_tier,
        tier_rate=tier_rate
    )
    return rule_tier.id

def update_secondary_rule_tier(id, tier_rate):
    SecondaryRuleTier.objects.filter(pk__exact=id).update(
        tier_rate=tier_rate  
        )

def delete_secondary_rule_tier(id):
    SecondaryRuleTier.objects.filter(pk__exact=id).delete()

# Calculations
def create_calculation(username, jurisdiction_ids, variable_table):
    calculation_result = TaxCalculationResult.objects.create(username=username)
    
    for jurisdiction_id in jurisdiction_ids:
        rulesets = RuleSet.objects.filter(jurisdiction_id__exact=jurisdiction_id).order_by('ordinal')
        for ruleset in rulesets:
            ruleset.calculate(variable_table, calculation_result)

    return calculation_result

def get_calculations_for_user(username):
    return TaxCalculationResult.objects.filter(username__exact=username).order_by('-created')