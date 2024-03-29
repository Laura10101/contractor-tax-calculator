"""Define models for the rules API."""

from django.db import models
from polymorphic.models import PolymorphicModel
from jurisdictions_api.models import Jurisdiction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class TaxCalculationResult(models.Model):
    """Create TaxCalculationResult model."""
    """Represents the complete set of results for a tax calculation."""

    username = models.CharField(max_length=255, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    excluded_jurisdiction_ids = models.CharField(
        max_length=255,
        null=False,
        blank=True
    )

    def add_ruleset_result(
        self,
        jurisdiction_id,
        tax_category_id,
        tax_category_name
    ):
        """Add results for a ruleset to the calculation results."""

        result = TaxRuleSetResult.objects.create(
            tax_calculation_result=self,
            jurisdiction_id=jurisdiction_id,
            tax_category_id=tax_category_id,
            tax_category_name=tax_category_name,
            ordinal=self.results.count()
        )
        return result


class TaxRuleSetResult(models.Model):
    """Create TaxRuleSetResult model."""
    """Represents the complete set of calculation results for a ruleset."""

    tax_calculation_result = models.ForeignKey(
        TaxCalculationResult,
        on_delete=models.CASCADE,
        related_name='results'
    )
    jurisdiction_id = models.IntegerField()
    tax_category_id = models.IntegerField()
    tax_category_name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    ordinal = models.IntegerField()

    def add_result(
        self,
        rule_id,
        rule_model_name,
        rule_name,
        variable_name,
        variable_value,
        taxable_amount,
        tax_rate,
        tax_payable,
        tier_id=None,
        tier_model_name=None,
        tier_name=None
    ):
        """Add the results of a rule calculation to ruleset calculations."""

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


class TaxRuleTierResult(models.Model):
    """Create TaxRuleTierResult model."""
    """Represents the results of a tax rule tier calculation."""

    ruleset_result = models.ForeignKey(
        TaxRuleSetResult,
        on_delete=models.CASCADE,
        related_name='results'
    )

    # Rules and rule tiers are polymorphic so instead of
    # holding object references, store the ids, names
    # and model types to simplify displaying the results in a consistent way
    rule_id = models.IntegerField()
    rule_model_name = models.CharField(max_length=255, null=False, blank=False)
    rule_name = models.CharField(max_length=255, null=False, blank=False)
    tier_id = models.IntegerField(null=True)
    tier_model_name = models.CharField(max_length=255, null=True, blank=False)
    tier_name = models.CharField(max_length=255, null=True, blank=False)

    variable_name = models.CharField(max_length=255, null=False, blank=False)
    variable_value = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )
    taxable_amount = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )
    tax_rate = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )
    tax_payable = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )
    ordinal = models.IntegerField()


class TaxCategory(models.Model):
    """Create TaxCategory model."""
    """Represents a type of tax."""

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )

    def __str__(self):
        """Represent the tax category as a string."""

        return self.name


class RuleSet(models.Model):
    """Create the RuleSet model."""
    """Groups the tax rates or rules for a given tax category"""
    """and jurisdiction."""

    jurisdiction_id = models.IntegerField()
    # Create foreign key for RuleSet/TaxCategory relationship
    tax_category = models.ForeignKey(TaxCategory, on_delete=models.CASCADE)
    ordinal = models.IntegerField(validators=[MinValueValidator(0)])

    def calculate(self, variable_table, calculation_result):
        if self.rules.count() > 0:
            ruleset_result = calculation_result.add_ruleset_result(
                jurisdiction_id=self.jurisdiction_id,
                tax_category_id=self.tax_category.id,
                tax_category_name=self.tax_category.name
            )

            rules = self.rules.order_by('ordinal')
            for rule in rules:
                rule.calculate(variable_table, ruleset_result)

    def validate(self, variable_table):
        rules = self.rules.order_by('ordinal')
        for rule in rules:
            rule.validate(variable_table)

    def __str__(self):
        return Jurisdiction.objects.get(
            pk=self.jurisdiction_id
        ).name + ' - ' + self.tax_category.name


class Rule(PolymorphicModel):
    """Create Rule model."""
    """Represents the rule for calculating a particular type of tax"""
    """in a particular jurisdiction."""
    """Base class for Rules."""

    ruleset = models.ForeignKey(
        RuleSet,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    # ordinal to indicate order in which rules are applied
    ordinal = models.IntegerField(validators=[MinValueValidator(0)])
    # Explanatory text box
    explainer = models.CharField(max_length=255, null=True, blank=True)
    # Indicates which value from the form submitted by the user this rule
    # should be applied to
    variable_name = models.CharField(max_length=255, null=False, blank=False)

    def validate(self, variable_table):
        """Ensure the variable table contains required variables."""

        if self.variable_name not in variable_table:
            raise ValidationError(
                "Variable " + self.variable_name +
                " was not found when validating rule " +
                str(self)
            )

        value = variable_table[self.variable_name]
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValidationError(
                "Value '" + value + "' is not valid for variable " +
                self.variable_name + " when validating rule " + str(self)
            )

    def __str__(self):
        """Represent the rule as a string."""

        return str(self.ruleset) + ' - ' + self.name


class FlatRateRule(Rule):
    """Create FlatRateRule model."""
    """Represents a tax rule which applies a flat rate"""
    """to a given income stream."""

    flat_rate = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0)]
    )

    def calculate(self, variable_table, ruleset_results):
        """Perform the calculation for the flat rate rule."""

        variable_value = variable_table[self.variable_name]
        tax_total = variable_value * (self.flat_rate / 100)

        # Add to the results dictionary
        ruleset_results.add_result(
            rule_id=self.id,
            rule_model_name='FlatRateRule',
            rule_name=str(self),
            variable_name=self.variable_name,
            variable_value=variable_value,
            taxable_amount=variable_value,
            tax_rate=self.flat_rate,
            tax_payable=tax_total
        )


class TieredRateRule(Rule):
    """Create TieredRateRule model."""
    """A tiered rate rule defines a number of tax"""
    """bands that apply different rates to each portion"""
    """of a given income stream."""

    def calculate(self, variable_table, ruleset_results):
        """Calculate the tax payable for a given tiered rate."""

        tiers = self.tiers.order_by('ordinal')
        variable = variable_table[self.variable_name]

        for tier in tiers:
            tier.calculate(variable, ruleset_results)


class RuleTier(models.Model):
    """Create RuleTier model."""
    """A rule tier represents a tax band for a tiered rate rule."""

    # Identify the rule to which this tier belongs
    rule = models.ForeignKey(
        TieredRateRule,
        on_delete=models.CASCADE,
        related_name='tiers'
    )
    # Create min and max value attributes for each tier
    min_value = models.IntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0)]
    )
    # This has to allow null as there will be no max value for some objects
    max_value = models.IntegerField(blank=True, null=True)
    ordinal = models.IntegerField()
    tier_rate = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )

    def calculate(self, variable, ruleset_results):
        """Calculate the tax payable for this tier."""

        max_value = self.max_value
        min_value = self.min_value
        print('variable=' + str(variable) + ', min_val=' + str(min_value))
        if variable >= min_value:
            if max_value is None:
                max_value = variable

            if variable < max_value:
                max_value = variable

            taxable_amount = max_value - min_value
            tax_subtotal = taxable_amount * (self.tier_rate / 100)

            print('Adding rule tier result')
            ruleset_results.add_result(
                rule_id=self.rule.id,
                rule_model_name='TieredRateRule',
                rule_name=str(self.rule),
                tier_id=self.id,
                tier_model_name='RuleTier',
                tier_name=str(self),
                variable_name=self.rule.variable_name,
                variable_value=variable,
                taxable_amount=round(taxable_amount, 2),
                tax_rate=self.tier_rate,
                tax_payable=round(tax_subtotal, 2)
            )

    def __str__(self):
        """Represent this rule tier as a string."""

        string = str(self.rule) + ' - Tier '
        string = string + str(self.min_value) + ' to '
        string = string + str(self.max_value)
        return string


class SecondaryTieredRateRule(Rule):
    """Create SecondaryTieredRateRule model."""
    """A secondary tiered rate rule taxes a second income stream"""
    """progressively based on a primary rule. The secondary rule"""
    """applies different tax rates to the same bands as the primary rule."""
    """The secondary rule starts calculating tax on the secondary income"""
    """from the point in the bands at which the primary income ends."""

    # Foreign key to primary rule that it is connected to
    primary_rule = models.ForeignKey(
        TieredRateRule,
        on_delete=models.DO_NOTHING,
        related_name='secondary_rules'
    )

    def calculate(self, variable_table, ruleset_results):
        """Calculate tax for the secondary tiered rate rule."""

        primary_income = variable_table[self.primary_rule.variable_name]
        secondary_income = variable_table[self.variable_name]

        if secondary_income > 0:
            tiers = self.tiers.order_by('primary_tier__ordinal')
            for tier in tiers:
                tier.calculate(
                    primary_income,
                    secondary_income,
                    ruleset_results
                )


class SecondaryRuleTier(models.Model):
    """Create SecondaryRuleTier model."""
    """Defines the tax rate for a tier in a secondary rule."""

    secondary_rule = models.ForeignKey(
        SecondaryTieredRateRule,
        on_delete=models.CASCADE,
        related_name='tiers'
    )
    primary_tier = models.ForeignKey(
        RuleTier,
        on_delete=models.DO_NOTHING,
        related_name='+'
    )
    tier_rate = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )
    ordinal = models.IntegerField()

    def calculate(self, primary_income, secondary_income, ruleset_results):
        """Calculate the tax payable on this secondary tier."""

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
                tier_diff = tier_min - primary_income
                secondary_income_remaining = secondary_income - tier_diff
            else:
                secondary_income_remaining = secondary_income

            # Now work out how much secondary income needs to be taxed
            # in this tier
            # If the secondary income remaining is greater than the amount
            # reamining for this tier then just all of the remaining tier
            # allowance will be used up, otherwise only tax the reamining
            # secondary income
            if secondary_income_remaining > tier_allowance_remaining:
                taxable_amount = tier_allowance_remaining
            else:
                taxable_amount = secondary_income_remaining

            tax_subtotal = taxable_amount * (self.tier_rate / 100)

            ruleset_results.add_result(
                rule_id=self.secondary_rule.id,
                rule_model_name='SecondaryTieredRateRule',
                rule_name=str(self.secondary_rule),
                tier_id=self.id,
                tier_model_name='SecondaryRuleTier',
                tier_name=str(self),
                variable_name=self.secondary_rule.variable_name,
                variable_value=secondary_income,
                taxable_amount=round(taxable_amount, 2),
                tax_rate=self.tier_rate,
                tax_payable=round(tax_subtotal, 2)
            )

    def __str__(self):
        """Represent this secondary rule tier as a string"""
        string = str(self.secondary_rule) + ' - Tier '
        string = string + str(self.primary_tier.min_value)
        string = string + ' to ' + str(self.primary_tier.max_value)
        return string
