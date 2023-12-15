import pandas

data = [
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tiered_rule_iteration_with_single_tier_defined - assert 2800 == 3000.0",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvkPE",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The test assumed that in this scenario the first unit of secondary income would be taxed within this tier. However, as the primary income fell below the tier minimum, this was not the case. Updated the test to reflect the fact that the first £1000 would be taxed below the tier.",
        "createdAt": "2023-12-15T14:21:30Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/105#issuecomment-1857962948",
        "viewerDidAuthor": True
      }
    ],
    "number": 105,
    "title": "Testing secondary tiered rule with single tier fails AssertionError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/105"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tiered_rule_iteration_with_single_tier_defined - django.db.utils.IntegrityError: NOT NULL constraint failed: rules_api_rule.ruleset_id",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvkDo",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Equality operator used to assign the primary rule's ruleset to the secondary rule. This was replaced with the assignment operator.",
        "createdAt": "2023-12-15T14:20:58Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/104#issuecomment-1857962216",
        "viewerDidAuthor": True
      }
    ],
    "number": 104,
    "title": "Testing secondary tiered rule with single tier fails with IntegrityError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/104"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_ruleset_iteration_with_multiple_rules_defined - assert 1 == 2",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvj6L",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The test was setting the salary to 9000 which was below the min_value for the tiered rate rule. The tiered rate rule was therefore not being applied. Increased the salary to 30000",
        "createdAt": "2023-12-15T14:20:32Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/103#issuecomment-1857961611",
        "viewerDidAuthor": True
      }
    ],
    "number": 103,
    "title": "Testing ruleset iteration with multiple rules fails as only one result created",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/103"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_ruleset_iteration_with_no_rules_defined - AssertionError: assert 1 == 0",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvjwL",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Added check to ensure rules exist within the ruleset before creating the RuleSet result",
        "createdAt": "2023-12-15T14:20:05Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/102#issuecomment-1857960971",
        "viewerDidAuthor": True
      }
    ],
    "number": 102,
    "title": "Testing ruleset iteration with no rules fails as test result created",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/102"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_tiered_rule_iteration_with_multiple_tiers_defined - assert 13499.550000000001 == 13499.55",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvjl6",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Added rounding to the calculate method for RuleTiers to round to 2 dp.",
        "createdAt": "2023-12-15T14:19:36Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/101#issuecomment-1857960314",
        "viewerDidAuthor": True
      }
    ],
    "number": 101,
    "title": "Iterating over tiered rate rule with multiple tiers fails due with AssertionError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/101"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_tiered_rule_iteration_with_multiple_tiers_defined - AssertionError: assert Decimal('13499.55') == 13499.55",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvjc1",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "TaxPayable and Tier Tax Rates are stored as a decimal value but floats are used outside of the Django models. Updated model to store tax_payable and variable_value and tier_rate as FloatField.",
        "createdAt": "2023-12-15T14:19:09Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/100#issuecomment-1857959733",
        "viewerDidAuthor": True
      }
    ],
    "number": 100,
    "title": "Iterating over tiered rate rule with multiple tiers fails due to DecimalField conversion",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/100"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_primary_income_on_lower_boundary_and_no_secondary_income - AssertionError: assert 1 == 0",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvjTm",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated SecondaryTieredRateRule to ignore tiers if no secondary income",
        "createdAt": "2023-12-15T14:18:42Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/99#issuecomment-1857959142",
        "viewerDidAuthor": True
      }
    ],
    "number": 99,
    "title": "Secondary tiered rate rule applies tiers where no secondary income",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/99"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - TypeError: TaxRuleSetResult.add_result() missing 1 required positional argument: 'variable_value'",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvjLE",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated SecondaryRuleTier to pass secondary income as variable value",
        "createdAt": "2023-12-15T14:18:17Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/98#issuecomment-1857958596",
        "viewerDidAuthor": True
      }
    ],
    "number": 98,
    "title": "Secondary rule tier calculate method not passing variable_value to add_result() method",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/98"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - NameError: name 'lower_limit' is not defined",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvjD8",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated reference to 'lower_limit' to use correct variable name ('tier_min')",
        "createdAt": "2023-12-15T14:17:57Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/97#issuecomment-1857958140",
        "viewerDidAuthor": True
      }
    ],
    "number": 97,
    "title": "Secondary rule tier tests failing with NameError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/97"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - TypeError: SecondaryRuleTier.calculate() missing 1 required positional argument: 'ruleset_results'",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvia0",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated the secondarytieredraterule calculate function to pass in both variables",
        "createdAt": "2023-12-15T14:16:00Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/96#issuecomment-1857955508",
        "viewerDidAuthor": True
      }
    ],
    "number": 96,
    "title": "Secondary rule was passing only the secondary income to the secondary tier calculate method",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/96"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - KeyError: ''",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uviSD",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Helper function was not setting the variable_name on the secondary rule",
        "createdAt": "2023-12-15T14:15:33Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/95#issuecomment-1857954947",
        "viewerDidAuthor": True
      }
    ],
    "number": 95,
    "title": "No variable name found when calculating SecondaryTier result",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/95"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - django.core.exceptions.FieldError: Cannot resolve keyword 'ordinal' into field. Choices are: id, primary_tier, primary_tier_id, secondary_rule, secondary_rule_i...",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uviGq",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "SecondaryRuleTier has no ordinal so updated to order by the related primary tier ordinal",
        "createdAt": "2023-12-15T14:15:01Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/94#issuecomment-1857954218",
        "viewerDidAuthor": True
      }
    ],
    "number": 94,
    "title": "Secondary rule tier tests failing to sort tiers by ordinal",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/94"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - django.db.utils.IntegrityError: UNIQUE constraint failed: jurisdictions_api_jurisdiction.name",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvh5o",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Added a count to the end of jurisdiction name to disambiguate",
        "createdAt": "2023-12-15T14:14:24Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/93#issuecomment-1857953384",
        "viewerDidAuthor": True
      }
    ],
    "number": 93,
    "title": "Secondary rule tier tests creating duplicate jurisdictions",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/93"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_secondary_tier_calculate_where_total_income_below_lower_boundary - django.db.utils.IntegrityError: NOT NULL constraint failed: rules_api_rule.ordinal",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvhol",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The create_mock_secondary_Tiered_Rate_Rule helper function was not setting mandatory fields on the new rule",
        "createdAt": "2023-12-15T14:13:33Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/92#issuecomment-1857952293",
        "viewerDidAuthor": True
      }
    ],
    "number": 92,
    "title": "Secondary rule tier tests fail with IntegrityError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/92"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_below_boundary - AssertionError: assert 1 == 0",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvhhP",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The RuleTier was not checking to ensure the variable was above the min_value before applying itself",
        "createdAt": "2023-12-15T14:13:10Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/91#issuecomment-1857951823",
        "viewerDidAuthor": True
      }
    ],
    "number": 91,
    "title": "Rule tier tests fail when variable < min_value",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/91"
  },
  {
    "body": "TypeError: TaxRuleSetResult.add_result() missing 1 required positional argument: 'variable_value'",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvhU0",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated the RuleTier to pass the variable_value to add_result",
        "createdAt": "2023-12-15T14:12:35Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/90#issuecomment-1857951028",
        "viewerDidAuthor": True
      }
    ],
    "number": 90,
    "title": "Rule tier tests fail with TypeError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/90"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_below_boundary - TypeError: '<' not supported between instances of 'dict' and 'int'",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvhHW",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The TieredRateRule was passing the variable table rather than the variable to the tier",
        "createdAt": "2023-12-15T14:11:59Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/89#issuecomment-1857950166",
        "viewerDidAuthor": True
      }
    ],
    "number": 89,
    "title": "Rule tier tests fail with TypeError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/89"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_below_boundary - rules_api.models.RuleTier.rule.RelatedObjectDoesNotExist: RuleTier has no rule.\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_on_lower_boundary - rules_api.models.RuleTier.rule.RelatedObjectDoesNotExist: RuleTier has no rule.\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_within_boundaries - rules_api.models.RuleTier.rule.RelatedObjectDoesNotExist: RuleTier has no rule.\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_on_upper_boundary - rules_api.models.RuleTier.rule.RelatedObjectDoesNotExist: RuleTier has no rule.\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_above_upper_boundary - rules_api.models.RuleTier.rule.RelatedObjectDoesNotExist: RuleTier has no rule.\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_no_upper_boundary_and_income_above_lower_boundary - rules_api.models.RuleTier.rule.RelatedObjectDoesNotExist: RuleTier has no rule.",
    "comments": [],
    "number": 88,
    "title": "Rule tier tests fail with RelatedObjectDoesNotExist",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/88"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_flat_rate_calculate - TypeError: object of type 'TaxRuleSetResult' has no len()",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvgn7",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The test needed to be updated to reflect the new models for storing tax results as opposed to the old dictionary.",
        "createdAt": "2023-12-15T14:10:25Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/87#issuecomment-1857948155",
        "viewerDidAuthor": True
      }
    ],
    "number": 87,
    "title": "Flat rate rule test fails with TypeError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/87"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_flat_rate_calculate - django.db.utils.IntegrityError: NOT NULL constraint failed: rules_api_taxruletierresult.tax_rate",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvgah",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The TaxRuleSetResult was not setting the tax_rate when creating the TaxRuleTierResult",
        "createdAt": "2023-12-15T14:09:47Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/86#issuecomment-1857947297",
        "viewerDidAuthor": True
      }
    ],
    "number": 86,
    "title": "Flat rate rule test fails with IntegrityError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/86"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_flat_rate_calculate - rules_api.models.Rule.ruleset.RelatedObjectDoesNotExist: Rule has no ruleset.. Did you mean: 'rule_ptr'?",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvgNk",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated test to create a fully instantiated ruleset and link this to the rule",
        "createdAt": "2023-12-15T14:09:12Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/85#issuecomment-1857946468",
        "viewerDidAuthor": True
      }
    ],
    "number": 85,
    "title": "Testing flat rate calculation fails with RelatedObjectDoesNotExist",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/85"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_flat_rate_calculate - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_below_boundary - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_on_lower_boundary - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_within_boundaries - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_on_upper_boundary - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_income_above_upper_boundary - AttributeError: 'NoneType' object has no attribute 'add_result'        \r\nFAILED rules_api/test_models.py::test_rule_tier_calculate_where_no_upper_boundary_and_income_above_lower_boundary - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_secondary_tier_calculate_where_primary_income_on_lower_boundary_and_total_within_boundaries - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_secondary_tier_calculate_where_primary_income_and_total_within_boundaries - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_secondary_tier_calculate_where_primary_income_within_boundaries_and_total_exceeds - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_secondary_tier_calculate_where_primary_income_on_upper_boundary_and_total_exceeds - AttributeError: 'NoneType' object has no attribute 'add_result'\r\nFAILED rules_api/test_models.py::test_secondary_tier_calculate_where_primary_income_above_upper_boundary - AttributeError: 'NoneType' object has no attribute 'add_result'",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvf_V",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "The helper function to create mock Ruleset results was not returning the created result object",
        "createdAt": "2023-12-15T14:08:27Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/84#issuecomment-1857945557",
        "viewerDidAuthor": True
      }
    ],
    "number": 84,
    "title": "Rule model tests failing with AttributeError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/84"
  },
  {
    "body": "FAILED rules_api/test_models.py::test_flat_rate_calculate - TypeError: 'int' object is not subscriptable",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uvfi7",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Test is passing an int variable instead of a variable dictionary. Updated the test to correct this.",
        "createdAt": "2023-12-15T14:07:28Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/83#issuecomment-1857943739",
        "viewerDidAuthor": True
      }
    ],
    "number": 83,
    "title": "Rule model tests failing with TypeError 'int' is not subscriptable",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/83"
  },
  {
    "body": "When confirming a payment via the Stripe API, the payment completes synchronously rather than asynchronously with a webhook posted back to the payment API.",
    "comments": [],
    "number": 82,
    "title": "Payment confirmation and completion is happening synchronously rather than via the webhook",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/82"
  },
  {
    "body": "FAILED payments_api/test_services.py::test_process_payment_success - payments_api.models.Payment.DoesNotExist\r\nFAILED payments_api/test_services.py::test_process_payment_failure - payments_api.models.Payment.DoesNotExist",
    "comments": [],
    "number": 81,
    "title": "Valid process payment tests failing with Payment.DoesNotExist",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/81"
  },
  {
    "body": "FAILED payments_api/test_services.py::test_process_payment_success_with_unknown_stripe_pid - Failed: DID NOT RAISE <class 'django.core.exceptions.ObjectDoesNotExist'>\r\nFAILED payments_api/test_services.py::test_process_payment_failure_with_unknown_stripe_pid - Failed: DID NOT RAISE <class 'django.core.exceptions.ObjectDoesNotExist'>",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uT1to",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated the tests to expect Payment.DoesNotExist, and updated code to check the number of payments matching the PID.",
        "createdAt": "2023-12-11T18:56:00Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/80#issuecomment-1850694504",
        "viewerDidAuthor": True
      }
    ],
    "number": 80,
    "title": "Processing payment with unknown stripe pid fails to raise expected error",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/80"
  },
  {
    "body": "FAILED payments_api/test_services.py::test_process_payment_success - django.core.exceptions.FieldDoesNotExist: Payment has no field named 'created_or_failed_date'\r\nFAILED payments_api/test_services.py::test_process_payment_success_with_unknown_stripe_pid - django.core.exceptions.FieldDoesNotExist: Payment has no field named 'created_or_failed_date'\r\nFAILED payments_api/test_services.py::test_process_payment_failure - django.core.exceptions.FieldDoesNotExist: Payment has no field named 'created_or_failed_date'\r\nFAILED payments_api/test_services.py::test_process_payment_failure_with_unknown_stripe_pid - django.core.exceptions.FieldDoesNotExist: Payment has no field named 'created_or_failed_date'",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uT0Jf",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Was attempting to access 'created_or_failed_date' in services. Updated to access 'completed_or_failed_date'",
        "createdAt": "2023-12-11T18:51:39Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/79#issuecomment-1850688095",
        "viewerDidAuthor": True
      }
    ],
    "number": 79,
    "title": "Process payment tests failing with FieldDoesNotExist error",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/79"
  },
  {
    "body": "FAILED payments_api/test_services.py::test_process_payment_success - TypeError: Field 'id' expected a number but got (1, 'pi_3OMETKFkVBiDxSnk1zlGaQoh_secret_O8UJhoD0S96IDBSUFRTq6WH4Z').\r\nFAILED payments_api/test_services.py::test_process_payment_failure - TypeError: Field 'id' expected a number but got (1, 'pi_3OMETLFkVBiDxSnk1rejsgjD_secret_CWy4lbdYkrDq613loEjBYE9sS').",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uTy7p",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "create_payment service returns two parameters, but only one was being collected.",
        "createdAt": "2023-12-11T18:48:19Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/78#issuecomment-1850683113",
        "viewerDidAuthor": True
      }
    ],
    "number": 78,
    "title": "Process payment tests failing with TypeError",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/78"
  },
  {
    "body": "FAILED payments_api/test_services.py::test_process_payment_success - NameError: name 'APIClient' is not defined",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uTxyx",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Imported APIClient from rest_framework.test",
        "createdAt": "2023-12-11T18:45:20Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/77#issuecomment-1850678449",
        "viewerDidAuthor": True
      }
    ],
    "number": 77,
    "title": "Process payment tests failing with NameError: 'APIClient'",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/77"
  },
  {
    "body": "FAILED payments_api/test_services.py::test_create_payment_with_null_subscription_id - Failed: DID NOT RAISE <class 'django.core.exceptions.ValidationError'>",
    "comments": [
      {
        "id": "IC_kwDOJVY7Ys5uSi4F",
        "author": {
          "login": "Laura10101"
        },
        "authorAssociation": "OWNER",
        "body": "Updated test to expect this to succeed as model explicitly allows subscription to be null. This is because a subscription may not exist for the user until after payment has completed if this is a new customer.",
        "createdAt": "2023-12-11T15:51:31Z",
        "includesCreatedEdit": False,
        "isMinimized": False,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/76#issuecomment-1850355205",
        "viewerDidAuthor": True
      }
    ],
    "number": 76,
    "title": "Creation service test fails when passing a null subscription_id",
    "url": "https://github.com/Laura10101/contractor-tax-calculator/issues/76"
  }
]

for bug in data:
    comments = ''
    for comment in bug['comments']:
        if len(comments) > 0:
            comments += "\\ "
        comments += comment['body']

    bug['Resolution'] = comments

df = pandas.DataFrame.from_dict(data).rename(columns={'number': 'GH ID', 'title': 'Title', 'body': 'Description', 'Resolution': 'Resolution', 'url': 'Github URL'})
df = df[['GH ID', 'Title', 'Description', 'Resolution', 'Github URL']]

f = open("BUGS.MD", "w")
f.write(df.to_markdown(index=False))
f.close()