"""Define service methods for rules API."""
from .models import *
from django.core.exceptions import ValidationError


def get_rulesets_by_jurisdiction_id(jurisdiction_id):
    """Return all rulesets for a given list of jurisdiction ids."""

    if not isinstance(jurisdiction_id, int):
        raise ValidationError(
            'jurisdiction_id must be a valid (non-negative, non-null) integer'
        )

    return RuleSet.objects.filter(
        jurisdiction_id__exact=jurisdiction_id
    ).order_by('ordinal')


def create_ruleset(jurisdiction_id, tax_category_id, ordinal):
    """Create a new ruleset for the given tax category & jurisdiction."""

    if not isinstance(jurisdiction_id, int):
        raise ValidationError(
            'jurisdiction_id must be a valid (non-negative, non-null) integer'
        )

    if RuleSet.objects.filter(
        jurisdiction_id__exact=jurisdiction_id,
        tax_category_id__exact=tax_category_id
    ).count() > 0:
        raise ValidationError(
            'A ruleset already exists for this tax category and jurisdiction'
        )
    # Assign tax category id to new rule set
    tax_category = TaxCategory.objects.get(pk=tax_category_id)
    # Create new ruleset in the database
    new_ruleset = RuleSet()
    new_ruleset.jurisdiction_id = jurisdiction_id
    new_ruleset.tax_category = tax_category
    new_ruleset.ordinal = ordinal
    new_ruleset.full_clean()
    new_ruleset.save()
    # Return ID of newly created ruleset
    return new_ruleset.id


def update_ruleset_ordinal(ruleset_id, ordinal):
    """Update an existing ruleset's ordinal."""

    if not isinstance(ordinal, int):
        raise ValidationError(
            'ordinal must be a valid (non-negative, non-null) integer'
        )

    ruleset = RuleSet.objects.get(pk=ruleset_id)
    ruleset.ordinal = ordinal
    ruleset.full_clean()
    ruleset.save()


def delete_ruleset(id):
    """Delete a ruleset based on its id."""

    # To avoid foreign key violations between secondary/tiered rate rules
    # delete all secondary rules first
    ruleset = RuleSet.objects.get(pk=id)

    # Delete rules manually to work around cascading delete issues in
    # Django polymorphic
    # https://github.com/jazzband/django-polymorphic/issues/229

    # To avoid the Django polymorphic issues and also any constraints
    # between tiered rate rules and secondary tiered rate rules, or
    # between secondary and primary rule tiers, delete rules individually.
    # Start with the atomic rule types (secondary tiered and flat rate)
    # and then do aggregate rule types (tiered rate)
    for rule in ruleset.rules.all():
        if isinstance(
            rule,
            SecondaryTieredRateRule
        ) or isinstance(rule, FlatRateRule):
            Rule.objects.get(pk=rule.id).delete()

    # Not all secondary rules referencing a given tiered rate rule will
    # be in the same ruleset so have to delete any secondary tiered rate
    # rules referencing the primary tiered rate rule
    for rule in ruleset.rules.all():
        if isinstance(rule, TieredRateRule):
            # Delete the secondary rules first
            for secondary_rule in rule.secondary_rules.all():
                Rule.objects.get(pk=secondary_rule.id).delete()

            Rule.objects.get(pk=rule.id).delete()

    # Finally, delete the ruleset
    ruleset.delete()


def delete_rulesets_for_jurisdiction(jurisdiction_id):
    """Delete all rulesets for a given jurisdiction ID."""

    rulesets = RuleSet.objects.filter(jurisdiction_id__exact=jurisdiction_id)
    for ruleset in rulesets.all():
        for rule in ruleset.rules.all():
            if isinstance(
                rule,
                TieredRateRule
            ) or isinstance(rule, SecondaryTieredRateRule):
                for tier in rule.tiers.all():
                    tier.delete()
            rule.delete()
        ruleset.delete()


def get_tax_categories():
    """Retrun a list of all tax categories."""
    return TaxCategory.objects.all()


def create_tax_category(name):
    """Create a new tax category."""
    tax_category = TaxCategory()
    tax_category.name = name
    tax_category.full_clean()
    tax_category.save()
    return tax_category.id


def delete_tax_category(id):
    """Delete a tax category based on its ID."""
    tax_category = TaxCategory.objects.get(pk=id)
    tax_category.delete()


def delete_rule(id):
    """Delete a rule of any type based on its ID."""
    rule = Rule.objects.get(pk=id)

    # Delete secondary tier rate rules if the rule to be deleted
    # is a tiered rate rule
    if isinstance(rule, TieredRateRule):
        # Delete the secondary rules first
        for secondary_rule in rule.secondary_rules.all():
            Rule.objects.get(pk=secondary_rule.id).delete()

    rule.delete()


def create_flat_rate_rule(
    ruleset_id,
    name,
    ordinal,
    explainer,
    variable_name,
    tax_rate
):
    """Create a new flat rate rule."""

    if not isinstance(ruleset_id, int):
        raise RuleSet.DoesNotExist(
            'ruleset_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')

    if not isinstance(tax_rate, float) and not isinstance(tax_rate, int):
        raise ValidationError(
            'tax_rate must be a non-negative floating point value'
        )

    ruleset = RuleSet.objects.get(pk=ruleset_id)

    print(variable_name)
    flat_rate_rule = FlatRateRule()
    flat_rate_rule.ruleset = ruleset
    flat_rate_rule.name = name
    flat_rate_rule.ordinal = ordinal
    flat_rate_rule.explainer = explainer
    flat_rate_rule.variable_name = variable_name
    flat_rate_rule.flat_rate = tax_rate
    flat_rate_rule.full_clean()
    flat_rate_rule.save()
    return flat_rate_rule.id


def update_flat_rate_rule(
    id,
    name,
    ordinal,
    explainer,
    variable_name,
    tax_rate
):
    """Update an existing flat rate rule."""

    if not isinstance(id, int):
        raise FlatRateRule.DoesNotExist(
            'rule_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError(
            'ordinal must be a non-negative integer value'
        )

    if not isinstance(tax_rate, float) and not isinstance(tax_rate, int):
        raise ValidationError(
            'tax_rate must be a non-negative integer value'
        )

    rule = FlatRateRule.objects.get(pk=id)
    rule.name = name
    rule.ordinal = ordinal
    rule.explainer = explainer
    rule.variable_name = variable_name
    rule.flat_rate = tax_rate
    rule.full_clean()
    rule.save()


def create_tiered_rate_rule(
    ruleset_id,
    name,
    ordinal,
    explainer,
    variable_name
):
    """Create a new tiered rate rule."""

    if not isinstance(ruleset_id, int):
        raise RuleSet.DoesNotExist(
            'ruleset_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError(
            'ordinal must be a non-negative integer value'
        )

    ruleset = RuleSet.objects.get(pk=ruleset_id)

    tiered_rate_rule = TieredRateRule()
    tiered_rate_rule.ruleset = ruleset
    tiered_rate_rule.name = name
    tiered_rate_rule.ordinal = ordinal
    tiered_rate_rule.explainer = explainer
    tiered_rate_rule.variable_name = variable_name
    tiered_rate_rule.full_clean()
    tiered_rate_rule.save()
    return tiered_rate_rule.id


def update_tiered_rate_rule(id, name, ordinal, explainer, variable_name):
    """Update an existing tiered rate rule."""

    if not isinstance(id, int):
        raise TieredRateRule.DoesNotExist(
            'rule_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError(
            'ordinal must be a non-negative integer value'
        )

    tiered_rate_rule = TieredRateRule.objects.get(pk=id)
    tiered_rate_rule.name = name
    tiered_rate_rule.ordinal = ordinal
    tiered_rate_rule.explainer = explainer
    tiered_rate_rule.variable_name = variable_name
    tiered_rate_rule.full_clean()
    tiered_rate_rule.save()


def create_rule_tier(rule_id, min_value, max_value, ordinal, tier_rate):
    """Create a new rule tier."""

    if not isinstance(rule_id, int):
        raise TieredRateRule.DoesNotExist(
            'rule_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError(
            'ordinal must be a non-negative integer value'
        )

    # Get the rule from the database based on the rule id
    rule = TieredRateRule.objects.get(pk=rule_id)
    rule_tier = RuleTier()
    rule_tier.rule = rule
    rule_tier.min_value = min_value
    rule_tier.max_value = max_value
    rule_tier.ordinal = ordinal
    rule_tier.tier_rate = tier_rate
    rule_tier.full_clean()
    rule_tier.save()
    return rule_tier.id


def update_rule_tier(id, min_value, max_value, ordinal, tier_rate):
    """Update an existing rule tier."""

    if not isinstance(id, int):
        raise RuleTier.DoesNotExist(
            'tier_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')

    rule_tier = RuleTier.objects.get(pk=id)
    rule_tier.min_value = min_value
    rule_tier.max_value = max_value
    rule_tier.ordinal = ordinal
    rule_tier.tier_rate = tier_rate
    rule_tier.full_clean()
    rule_tier.save()


def delete_rule_tier(id):
    """Delete an existing rule tier based on its ID."""

    tier = RuleTier.objects.get(pk=id)
    tier.delete()


def create_secondary_tiered_rate_rule(
    ruleset_id,
    primary_rule_id,
    name,
    ordinal,
    explainer,
    variable_name
):
    """Create a new secondary tiered rate rule."""

    if not isinstance(ruleset_id, int):
        raise RuleSet.DoesNotExist(
            'ruleset_id must be a non-negative integer value'
        )

    if not isinstance(primary_rule_id, int):
        raise TieredRateRule.DoesNotExist(
            'primary_rule_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError(
            'ordinal must be a non-negative integer value'
        )

    ruleset = RuleSet.objects.get(pk=ruleset_id)

    primary_rule = TieredRateRule.objects.get(pk=primary_rule_id)
    secondary_tiered_rate_rule = SecondaryTieredRateRule()
    secondary_tiered_rate_rule.ruleset = ruleset
    secondary_tiered_rate_rule.primary_rule = primary_rule
    secondary_tiered_rate_rule.name = name
    secondary_tiered_rate_rule.ordinal = ordinal
    secondary_tiered_rate_rule.explainer = explainer
    secondary_tiered_rate_rule.variable_name = variable_name
    secondary_tiered_rate_rule.full_clean()
    secondary_tiered_rate_rule.save()
    return secondary_tiered_rate_rule.id


def update_secondary_tiered_rate_rule(
    id,
    name,
    ordinal,
    explainer,
    variable_name
):
    """Update an existing secondary tiered rate rule."""

    if not isinstance(id, int):
        raise SecondaryTieredRateRule.DoesNotExist(
            'rule_id must be a non-negative integer value'
        )

    if not isinstance(ordinal, int):
        raise ValidationError('ordinal must be a non-negative integer value')

    secondary_tiered_rate_rule = SecondaryTieredRateRule.objects.get(pk=id)
    secondary_tiered_rate_rule.name = name
    secondary_tiered_rate_rule.ordinal = ordinal
    secondary_tiered_rate_rule.explainer = explainer
    secondary_tiered_rate_rule.variable_name = variable_name
    secondary_tiered_rate_rule.full_clean()
    secondary_tiered_rate_rule.save()


def create_secondary_rule_tier(
    secondary_rule_id,
    primary_tier_id,
    ordinal,
    tier_rate
):
    """Create a new secondary rule tier."""

    if not isinstance(secondary_rule_id, int):
        raise SecondaryTieredRateRule.DoesNotExist(
            'rule_id must be a non-negative integer value'
        )

    if not isinstance(primary_tier_id, int):
        raise RuleTier.DoesNotExist(
            'primary_tier_id must be a non-negative integer value'
        )

    # Get the primary rule object from the database based on the rule tier id
    secondary_rule = SecondaryTieredRateRule.objects.get(pk=secondary_rule_id)
    primary_tier = RuleTier.objects.get(pk=primary_tier_id)
    secondary_rule_tier = SecondaryRuleTier()
    secondary_rule_tier.secondary_rule = secondary_rule
    secondary_rule_tier.primary_tier = primary_tier
    secondary_rule_tier.tier_rate = tier_rate
    secondary_rule_tier.ordinal = ordinal
    secondary_rule_tier.full_clean()
    secondary_rule_tier.save()
    return secondary_rule_tier.id


def update_secondary_rule_tier(id, ordinal, tier_rate):
    """Update an existing secondary rule tier."""

    if not isinstance(id, int):
        raise SecondaryRuleTier.DoesNotExist(
            'tier_id must be a non-negative integer value'
        )

    secondary_rule_tier = SecondaryRuleTier.objects.get(pk=id)
    secondary_rule_tier.ordinal = ordinal
    secondary_rule_tier.tier_rate = tier_rate
    secondary_rule_tier.full_clean()
    secondary_rule_tier.save()


def delete_secondary_rule_tier(id):
    """Delete an existing secondary rule tier based on its ID."""

    tier = SecondaryRuleTier.objects.get(pk=id)
    tier.delete()


def create_calculation(username, jurisdiction_ids, variable_table):
    """Create a new calculation for the specified jurisdiction IDs and user."""
    if not isinstance(jurisdiction_ids, list) or len(jurisdiction_ids) == 0:
        raise ValidationError(
            'jurisdictions_ids must be a non-empty list of integers'
        )

    calculation_result = TaxCalculationResult()
    calculation_result.username = username
    calculation_result.full_clean()
    calculation_result.save()

    # Validate the variable table
    for jurisdiction_id in jurisdiction_ids:
        if not isinstance(jurisdiction_id, int):
            raise ValidationError(
                'jurisdiction_ids must be a valid list of integers'
            )

        rulesets = RuleSet.objects.filter(
            jurisdiction_id__exact=jurisdiction_id
        ).order_by('ordinal')
        for ruleset in rulesets:
            print(str(ruleset))
            ruleset.validate(variable_table)

    # Apply the calculation
    excluded_jurisdiction_ids = []
    for jurisdiction_id in jurisdiction_ids:
        rulesets = RuleSet.objects.filter(
            jurisdiction_id__exact=jurisdiction_id
        ).order_by('ordinal')
        if rulesets.count() == 0:
            excluded_jurisdiction_ids.append(jurisdiction_id)
        else:
            has_rules = False
            for ruleset in rulesets:
                if ruleset.rules.count() > 0:
                    has_rules = True
                ruleset.calculate(variable_table, calculation_result)

            if not has_rules:
                excluded_jurisdiction_ids.append(jurisdiction_id)
    excluded_id_strs = [str(val) for val in excluded_jurisdiction_ids]
    excluded_id_str = ','.join(excluded_id_strs)
    calculation_result.excluded_jurisdiction_ids = excluded_id_str

    return calculation_result


def get_calculations_for_user(username):
    """Get a list of tax calculations for the given user."""
    return TaxCalculationResult.objects.filter(
        username__exact=username
    ).order_by('-created')


def get_calculation_by_id(id):
    """Get a specific calculation based on its ID."""
    return TaxCalculationResult.objects.get(pk=id)
