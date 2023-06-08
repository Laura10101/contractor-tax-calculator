from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.

# This class contains the types of tax categories
class TaxCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

# This class is to group all the rules for a particular tax category in 
# a given jurisdiction
class RuleSet(models.Model):
    jurisdiction_id = models.IntegerField()
    # Create foreign key for RuleSet/TaxCategory relationship 
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.CASCADE)

# This class is the parent class for the different types of rules 
class Rule(PolymorphicModel): 
    name = models.CharField(max_length=255, null=False, blank=False)
    # ordinal to indicate order in which rules are applied  
    ordinal = models.IntegerField()
    # Explanatory text box 
    explainer = models.CharField(max_length=255, null=False, blank=False)
    # Indicates which value from the form submitted by the user this rule 
    # should be applied to 
    variable_name = models.CharField(max_length=255, null=False, blank=False)

# This class applies flat tax rates 
class FlatRateRule(Rule):
    flat_rate = models.DecimalField(decimal_places=2, max_digits=5)

    def calculate(self, variable_table, results_table):
        tax_total = variable_table[self.variable_name] * (flat_rate / 100)

# This class applies tiered rates of tax
class TieredRateRule(Rule):
    
    def calculate(self, variable_table, results_table):
        pass

# This class represents a single tax tier within a tiered rate rule
class RuleTier(models.Model):
    # Identify the rule to which this tier belongs
    rule = models.ForeignKey(TieredRateRule, on_delete=models.CASCADE)
    # Create min and max value attributes for each tier 
    min_value = models.IntegerField()
    # This has to allow null as there will be no max value for some objects
    max_value = models.IntegerField(blank=True, null=True)
    ordinal = models.IntegerField()
    tier_rate = models.DecimalField(decimal_places=2, max_digits=5)

    def calculate(self, variable, results_table):
        max_value = self.max_value

        if max_value == None:
            max_value = variable

        if variable < max_value:
            max_value = variable

        tax_subtotal = (max_value - self.min_value) * (self.tier_rate / 100)

# This class represents a tiered rate rule that depends on another tiered rate tule
# e.g. uk dividend tax 
# The particular feature of this type of rule is that it picks up from the point
# in the tiering where the primary tier rule left off 

class SecondaryTieredRateRule(Rule):
    # Foreign key to primary rule that it is connected to 
    primary_rule = models.ForeignKey(TieredRateRule, on_delete=models.CASCADE)

    def calculate(self, variable_table, results_table):
        pass

# This class represents a tier of a secondary tiered rate rule 
class SecondaryRuleTier(models.Model):
    secondary_rule = models.ForeignKey(SecondaryTieredRateRule, on_delete=models.CASCADE)
    primary_tier = models.ForeignKey(RuleTier, on_delete=models.CASCADE)
    tier_rate = models.DecimalField(decimal_places=2, max_digits=5)

    def calculate(self, variable, results_table):
        pass
