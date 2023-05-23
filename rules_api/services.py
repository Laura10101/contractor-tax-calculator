from .models import *

### RULE SETS ###
# Create rule set
def create_ruleset(jurisdiction_id, tax_category_id):
    pass

# Delete rule set 
def delete_ruleset(id):
    pass

### TAX CATEGORIES ###
# Create tax category
def create_tax_category(name):
    pass

# Delete tax category
def delete_tax_category(id):
    pass

### FLAT RATE RULES ###
# Create rule 
def create_flat_rate_rule(name, ordinal, explainer, variable_name, tax_rate):
    pass

# Update rule 
def update_flat_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate):
    pass 

# Delete rule 
def delete_flat_rate_rule(id):
    pass

### TIERED RATE RULES ###
def create_tiered_rate_rule(name, ordinal, explainer, variable_name, tiers):
    pass

def update_tiered_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate, tiers):
    pass

def delete_tiered_rate_rule(id):
    pass

### SECONDARY TIERED RATE RULES ###
def create_secondary_tiered_rate_rule(name, ordinal, explainer, variable_name, tiers):
    pass

def update_secondary_tiered_rate_rule(id, name, ordinal, explainer, variable_name, tax_rate, tiers):
    pass

def delete_secondary_tiered_rate_rule(id):
    pass