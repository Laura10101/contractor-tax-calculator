from django.db import models
from polymorphic.models import PolymorphicModel
from jurisdictions_api.models import Jurisdiction
from django.core.validators import MinValueValidator
# Create your models here.
# This class contains the results for a given calculation across all jurisdictions in the comparison
class TaxCalculationResult(models.Model):
    username = models.CharField(max_length=255, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def add_ruleset_result(self, jurisdiction_id, tax_category_id, tax_category_name):
        result = TaxRuleSetResult.objects.create(
            tax_calculation_result = self,
            jurisdiction_id=jurisdiction_id,
            tax_category_id = tax_category_id,
            tax_category_name = tax_category_name,
            ordinal = self.results.count()
        )
        return result

# This class contains the tax calculation results for a given ruleset within a given jursidction
class TaxRuleSetResult(models.Model):
    tax_calculation_result = models.ForeignKey(TaxCalculationResult, on_delete=models.CASCADE, related_name='results')
    jurisdiction_id = models.IntegerField()
    tax_category_id = models.IntegerField()
    tax_category_name = models.CharField(max_length=255, null=False, blank=False)
    ordinal = models.IntegerField()

    def add_result(self, rule_id, rule_model_name, rule_name, variable_name, variable_value, taxable_amount,
        tax_rate, tax_payable, tier_id=None, tier_model_name=None, tier_name=None):
        result = TaxRuleTierResult.objects.create(
            ruleset_result=self,
            rule_id=rule_id,
            rule_model_name=rule_model_name,
            tier_id=tier_id,
            tier_model_name=tier_model_name,
            tier_name=tier_name,
            variable_name=variable_name,
            variable_value=variable_value,
            taxable_amount=taxable_amount,
            tax_rate=tax_rate,
            tax_payable=tax_payable,
            ordinal=self.results.count()
        )

# This class contains the tax calculation results for a given rule tier (for flat rate rules, there will only be one result for the rule)
class TaxRuleTierResult(models.Model):
    ruleset_result = models.ForeignKey(TaxRuleSetResult, on_delete=models.CASCADE, related_name='results')

    # Rules and rule tiers are polymorphic so instead of holding object references,
    # store the ids, names and model types to simplify displaying the results in a consistent way
    rule_id = models.IntegerField()
    rule_model_name = models.CharField(max_length=255, null=False, blank=False)
    rule_name = models.CharField(max_length=255, null=False, blank=False)
    tier_id = models.IntegerField(null = True)
    tier_model_name = models.CharField(max_length=255, null=True, blank=False)
    tier_name = models.CharField(max_length=255, null=True, blank=False)

    variable_name = models.CharField(max_length=255, null=False, blank=False)
    variable_value = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.0)])
    taxable_amount = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.0)])
    tax_rate = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.0)])
    tax_payable = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.0)])
    ordinal = models.IntegerField()

# This class contains the types of tax categories
class TaxCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

# This class is to group all the rules for a particular tax category in 
# a given jurisdiction
class RuleSet(models.Model):
    jurisdiction_id = models.IntegerField()
    # Create foreign key for RuleSet/TaxCategory relationship 
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.CASCADE)
    ordinal = models.IntegerField(validators=[MinValueValidator(0)])

    def calculate(self, variable_table, calculation_result):
        if self.rules.count() > 0:
            ruleset_result = calculation_result.add_ruleset_result(
                jurisdiction_id = self.jurisdiction_id,
                tax_category_id = self.tax_category.id,
                tax_category_name = self.tax_category.name
            )

            rules = self.rules.order_by('ordinal')
            for rule in rules:
                rule.calculate(variable_table, ruleset_result)


    def __str__(self):
        return Jurisdiction.objects.get(pk=self.jurisdiction_id).name + ' - ' + self.tax_category.name

# This class is the parent class for the different types of rules 
class Rule(PolymorphicModel): 
    ruleset = models.ForeignKey(RuleSet, on_delete=models.CASCADE, related_name='rules')
    name = models.CharField(max_length=255, null=False, blank=False)
    # ordinal to indicate order in which rules are applied  
    ordinal = models.IntegerField()
    # Explanatory text box 
    explainer = models.CharField(max_length=255, null=True, blank=True)
    # Indicates which value from the form submitted by the user this rule 
    # should be applied to 
    variable_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.ruleset) + ' - ' + self.name


# This class applies flat tax rates 
class FlatRateRule(Rule):
    flat_rate = models.DecimalField(decimal_places=2, max_digits=5)

    def calculate(self, variable_table, ruleset_results):
        variable_value = variable_table[self.variable_name]
        tax_total = variable_value * (self.flat_rate / 100)

        # Add to the results dictionary
        print('Adding flat rate rule result')
        ruleset_results.add_result(
            rule_id=self.id,
            rule_model_name='FlatRateRule',
            rule_name = str(self),
            variable_name = self.variable_name,
            variable_value = variable_value,
            taxable_amount = variable_value,
            tax_rate=self.flat_rate,
            tax_payable = tax_total
        )

# This class applies tiered rates of tax
class TieredRateRule(Rule):
    
    def calculate(self, variable_table, ruleset_results):
        tiers = self.tiers.order_by('ordinal')
        variable = variable_table[self.variable_name]

        for tier in tiers:
            tier.calculate(variable, ruleset_results)

# This class represents a single tax tier within a tiered rate rule
class RuleTier(models.Model):
    # Identify the rule to which this tier belongs
    rule = models.ForeignKey(TieredRateRule, on_delete=models.CASCADE, related_name='tiers')
    # Create min and max value attributes for each tier 
    min_value = models.IntegerField()
    # This has to allow null as there will be no max value for some objects
    max_value = models.IntegerField(blank=True, null=True)
    ordinal = models.IntegerField()
    tier_rate = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.0)])

    def calculate(self, variable, ruleset_results):
        max_value = self.max_value
        min_value = self.min_value
        print('variable=' + str(variable) + ', min_val=' + str(min_value))
        if variable >= min_value:
            print('Processing tier...')
            if max_value == None:
                max_value = variable

            if variable < max_value:
                max_value = variable

            taxable_amount = max_value - min_value
            tax_subtotal = taxable_amount * (self.tier_rate / 100)

            print('Adding rule tier result')
            ruleset_results.add_result(
                rule_id = self.rule.id,
                rule_model_name = 'TieredRateRule',
                rule_name = str(self.rule),
                tier_id = self.id,
                tier_model_name = 'RuleTier',
                tier_name = str(self),
                variable_name = self.rule.variable_name,
                variable_value = variable,
                taxable_amount = round(taxable_amount, 2),
                tax_rate = self.tier_rate,
                tax_payable = round(tax_subtotal, 2)
            )

    def __str__(self):
        return str(self.rule) + ' - Tier ' + str(self.min_value)  + ' to ' + str(self.max_value)

# This class represents a tiered rate rule that depends on another tiered rate tule
# e.g. uk dividend tax 
# The particular feature of this type of rule is that it picks up from the point
# in the tiering where the primary tier rule left off 

class SecondaryTieredRateRule(Rule):
    # Foreign key to primary rule that it is connected to 
    primary_rule = models.ForeignKey(TieredRateRule, on_delete=models.CASCADE)

    def calculate(self, variable_table, ruleset_results):
        primary_income = variable_table[self.primary_rule.variable_name]
        secondary_income = variable_table[self.variable_name]

        if secondary_income > 0:
            tiers = self.tiers.order_by('primary_tier__ordinal')
            for tier in tiers:
                tier.calculate(primary_income, secondary_income, ruleset_results)

# This class represents a tier of a secondary tiered rate rule 
class SecondaryRuleTier(models.Model):
    secondary_rule = models.ForeignKey(SecondaryTieredRateRule, on_delete=models.CASCADE, related_name='tiers')
    primary_tier = models.ForeignKey(RuleTier, on_delete=models.CASCADE, related_name='+')
    tier_rate = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0.0)])

    def calculate(self, primary_income, secondary_income, ruleset_results):
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
                secondary_income_remaining = secondary_income - (tier_min - primary_income)
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

            ruleset_results.add_result(
                rule_id = self.secondary_rule.id,
                rule_model_name = 'SecondaryTieredRateRule',
                rule_name = str(self.secondary_rule),
                tier_id = self.id,
                tier_model_name = 'SecondaryRuleTier',
                tier_name = str(self),
                variable_name = self.secondary_rule.variable_name,
                variable_value = secondary_income,
                taxable_amount = round(taxable_amount, 2),
                tax_rate = self.tier_rate,
                tax_payable = round(tax_subtotal, 2)
            )

    def __str__(self):
        return str(self.secondary_rule) + ' - Tier ' + str(self.primary_tier.min_value)  + ' to ' + str(self.primary_tier.max_value)