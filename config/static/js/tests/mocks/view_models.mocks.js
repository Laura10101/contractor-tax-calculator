const jurisdictions = [
    { id: 1, name: "All Jurisdictions" },
    { id: 2, name: "France" },
    { id: 3, name: "Germany" },
    { id: 4, name: "Dubai" },
    { id: 5, name: "Japan" }
];

const taxCategories = [
    { tax_category_id: 1, name: "Dividend Tax" },
    { tax_category_id: 2, name: "Corporation Tax" },
    { tax_category_id: 3, name: "Income Tax" },
    { tax_category_id: 4, name: "VAT" }
];

const forms = {
    "forms": {
      "1": {
        id: 1,
        jurisdiction_id: 1,
        questions: [
          {
            id: 3,
            text: "A boolean question test",
            explainer: "Created by automated test",
            is_mandatory: true,
            variable_name: "boolean_var",
            ordinal: 1,
            type: "boolean"
          },
          {
            id: 4,
            text: "A numeric question test",
            explainer: "Created by automated test",
            is_mandatory: true,
            variable_name: "numeric_var",
            ordinal: 2,
            type: "numeric",
            is_integer: true,
            min_value: 1,
            max_value: 100
          },
          {
            id: 7,
            text: "A multiple choice test",
            explainer: "Created by automated test",
            is_mandatory: true,
            variable_name: "multiple_choice_var",
            ordinal: 3,
            type: "multiple_choice",
            options: []
          }
        ]
      }
    }
};

const rules = [
    {
        id: 23,
        name: "France - Income Tax",
        tax_category_id: 1,
        ordinal: 1,
        rules: [
            {
                id: 13,
                name: "Income Tax Bands",
                explainer: "test_explainer",
                ordinal: 1,
                variable_name: "salary",
                type: "tiered_rate",
                tiers: []
            },
            {
                id: 219,
                name: "A Completely Mock rule",
                explainer: "test_explainer",
                ordinal: 1,
                variable_name: "numeric_var",
                taxRate: 20,
                type: "test_type"
            }
        ]
    },
    {
        id: 24,
        name: "France - Dividend Tax",
        tax_category_id: 2,
        ordinal: 2,
        rules: [
            {
                id: 15,
                name: "Dividend Tax Bands",
                explainer: "",
                ordinal: 1,
                variable_name: "dividends",
                primary_rule: {
                    id: 13,
                    name: "Income Tax Bands",
                    explainer: "test_explainer",
                    ordinal: 1,
                    variable_name: "salary",
                    type: "tiered_rate",
                    tiers: []
                },
                type: "secondary_tiered_rate",
                tiers: [],
                primary_rule_id: 13
            }
        ]
    },
    {
        id: 26,
        name: "France - Corporation Tax",
        tax_category_id: 3,
        ordinal: 3,
        rules: [
            {
                id: 19,
                name: "Corporation Tax",
                explainer: "",
                ordinal: 1,
                variable_name: "corporate_profits",
                type: "flat_rate",
                tax_rate: 25.0
            }
        ]
    },
    {
        id: 27,
        name: "France - VAT",
        tax_category_id: 4,
        ordinal: 4,
        rules: [
            {
                id: 41,
                name: "Rule 1",
                explainer: "",
                ordinal: 1,
                variable_name: "var1",
                type: "flat_rate",
                tax_rate: 20.0
            },
            {
                id: 44,
                name: "Rule 2",
                explainer: "",
                ordinal: 2,
                variable_name: "var 2",
                type: "tiered_rate",
                tiers: [
                    {
                        id: 3,
                        min_value: 0,
                        max_value: 15000,
                        ordinal: 1,
                        tier_rate: 12.0
                    },
                    {
                        id: 4,
                        min_value: 15001,
                        max_value: 25000,
                        ordinal: 2,
                        tier_rate: 22.0
                    },
                    {
                        id: 5,
                        min_value: 25001,
                        max_value: 45000,
                        ordinal: 3,
                        tier_rate: 25.0
                    },
                    {
                        id: 6,
                        min_value: 45001,
                        max_value: 60000,
                        ordinal: 4,
                        tier_rate: 30.0
                    }
                ]
            },
            {
                id: 45,
                name: "Rule 3",
                explainer: "",
                ordinal: 3,
                variable_name: "var_3",
                primary_rule: {
                    id: 44,
                    name: "Rule 2",
                    explainer: "",
                    ordinal: 2,
                    variable_name: "var 2",
                    type: "tiered_rate",
                    tiers: [
                        {
                            id: 3,
                            min_value: 0,
                            max_value: 15000,
                            ordinal: 1,
                            tier_rate: 12.0
                        },
                        {
                            id: 4,
                            min_value: 15001,
                            max_value: 25000,
                            ordinal: 2,
                            tier_rate: 22.0
                        },
                        {
                            id: 5,
                            min_value: 25001,
                            max_value: 45000,
                            ordinal: 3,
                            tier_rate: 25.0
                        },
                        {
                            id: 6,
                            min_value: 45001,
                            max_value: 60000,
                            ordinal: 4,
                            tier_rate: 30.0
                        }
                    ]
                },
                type: "secondary_tiered_rate",
                tiers: [
                    {
                        id: 1,
                        tier_rate: 9.0,
                        ordinal: 1,
                        primary_tier_id: 3
                    }
                ],
                primary_rule_id: 44
            }
        ]
    }
];

function deepClone(object) {
    // Deep clone code taken from:
    // https://developer.mozilla.org/en-US/docs/Glossary/Deep_copy
    return JSON.parse(JSON.stringify(object));
}

function buildAppState() {
    return {
        jurisdictions: deepClone(jurisdictions),
        taxCategories: deepClone(taxCategories),
        jurisdictionForm: deepClone(forms),
        jurisdictionRules: deepClone(rules)
    }
}

module.exports = { buildAppState };