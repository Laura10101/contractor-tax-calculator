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

    def calculate(self, primary_income, secondary_income, results_table):
        # Get the tier max and mins from the primary tier
        # and calculate total income
        tier_min = self.primary_tier.min_value
        tier_max = self.primary_tier.max_value
        total_income = primary_income + secondary_income

        # Check to see if this tier applies
        if total_income >= tier_min and primary_income < tier_max:
            # Work out how much of this tier has not yet been used
            # by the primary income
            if primary_income >= tier_min:
                tier_allowance_remaining = tier_max - primary_income
            else:
                tier_allowance_remaining = tier_max - tier_min

            # Now work out how much of the secondary allowance
            # hasn't yet been taxed by lower tiers
            # If the primary income falls within this tier then
            # none of the secondary income has been taxed
            # Otherwise the difference between this tier's lower limit
            # and the primary income gives the amount of the secondary income
            # that has been taxed by lower tiers
            if primary_income < tier_min:
                secondary_income_remaining = secondary_income - (lower_limit - primary_income)
            else:
                secondary_income_remaining = secondary_income

            # Now work out how much secondary income needs to be taxed
            # in this tier
            # If the secondary income remaining is greater than the amount
            # reamining for this tier then just all of the remaining tier allowance
            # will be used up, otherwise only tax the reamining secondary income
            if secondary_income_remaining > tier_allowance_remaining:
                taxable_amount = tier_allowance_remaining
            else:
                taxable_amount = secondary_income_remaining

            tax_subtotal = taxable_amount * (self.tier_rate / 100)