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

# Delete rule 
def delete_flat_rate_rule(id):
    FlatRateRule.objects.filter(pk__exact=id).delete()

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

def delete_tiered_rate_rule(id):
    TieredRateRule.objects.filter(pk__exact=id).delete()

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

def update_rule_tier():
    RuleTier.objects.filter(pk__exact=id).update(
        min_value=min_value,
        max_value=max_value,
        ordinal=ordinal,
        tier_rate=tier_rate   
        )
    
def delete_rule_tier(id):
    RuleTier.objects.filter(pk__exact=id).delete()

### SECONDARY TIERED RATE RULES ###
def create_secondary_tiered_rate_rule(name, ordinal, explainer, variable_name):
    secondary_tiered_rate_rule = SecondaryTieredRateRule.objects.create(
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

def delete_secondary_tiered_rate_rule(id):
    SecondaryTieredRateRule.objects.filter(pk__exact=id).delete()

### SECONDARY RULE TIER ###
def create_secondary_rule_tier(primary_tier_id, tier_rate):
    # Get the primary rule object from the database based on the rule tier id
    primary_tier = RuleTier.objects.get(pk=primary_tier_id)
    secondary_rule_tier = SecondaryRuleTier.objects.create(
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