/*
 * view_consts.js
 * Defines constants used to simplify access to key DOM elements and other resources
 */
/*
 * Model state constants
 */
const dialogStates = {
    modes: {
        create: "create",
        edit: "edit",
        delete: "delete"
    },

    entityTypes: {
        booleanQuestion: "boolean_question",
        numericQuestion: "numeric_question",
        multipleChoiceQuestion: "multiple_choice_question",
        multipleChoiceOption: "multiple_choice_option",
        ruleset: "ruleset",
        flatRateRule: "flat_rate_rule",
        tieredRateRule: "tiered_rate_rule",
        secondaryTieredRateRule: "secondary_tiered_rate_rule",
        ruleTier: "rule_tier",
        secondaryRuleTier: "secondary_rule_tier"
    }
};

/*
 * HTTP constants
 */
const endpoints = {
    jurisdictions: {
        base: "jurisdictions/"
    },

    forms: {
        base: "forms/",
        questions: function(form_id) {
            return "forms/" + form_id + "/questions/";
        },
        multipleChoiceOptions: function(formId, questionId) {
            return "forms/" + formId + "/questions/" + questionId + "/options/";
        }
    },

    rules: {
        base: "rules/",
        rulesets: "rules/rulesets/",
        rules: function(rulesetId) {
            return "rules/rulesets/" + rulesetId + "/rules/";
        },
        tiers: function(rulesetId, ruleId) {
            return "rules/rulesets/" + rulesetId + "/rules/" + ruleId + "/tiers/";
        },
        secondaryTiers: function(rulesetId, ruleId) {
            return "rules/rulesets/" + rulesetId + "/rules/" + ruleId + "/seocndarytiers/";
        },
        taxCategories: "rules/taxcategories/"
    }
};

/*
 * Status Modal Constants
 */
const statusDialog = {
    dialog: {
        id: "status-modal"
    },

    label: {
        id: "status-modal-label"
    },

    message: {
        id: "status-modal-message"
    }
};

/*
 * Confirmation Modal Constants
 */
const confirmationDialog = {
    dialog: {
        id: "confirmation-modal"
    },

    label: {
        id: "confirmation-modal-label"
    },

    message: {
        id: "confirmation-modal-message"
    },

    confirmationButton: {
        id: "confirmation-modal-confirm-btn"
    }
};

/*
 * Jurisdiction Select Constants
 */
const jurisdictionsSelect = {
    id: "jurisdictions-select"
};

/*
 * Question Dialog Constants
 */
const questionTypeDialog = {
    dialog: {
        id: "question-type-modal"
    },

    label: {
        id: "question-type-modal-label"
    },

    questionType: {
        label: {
            id: "question-type-modal-input-label"
        },

        input: {
            id: "question-type-modal-input"
        }
    }
};

const booleanQuestionDialog = {
    dialog: {
        id: "boolean-question-modal"
    },

    label: {
        id: "boolean-question-modal-label"
    },

    questionText: {
        label: {
            id: "boolean-question-modal-question-text-label"
        },
        input: {
            id: "boolean-question-modal-question-text-input"
        }
    },

    explainer: {
        label: {
            id: "boolean-question-modal-explainer-label"
        },
        input: {
            id: "boolean-question-modal-explainer-input"
        }
    },

    variableName: {
        label: {
            id: "boolean-question-modal-variable-name-label"
        },
        input: {
            id: "boolean-question-modal-variable-name-input"
        }
    },

    isMandatory: {
        label: {
            id: "boolean-question-modal-mandatory-label"
        },
        input: {
            id: "boolean-question-modal-mandatory-input"
        }
    }
};

const numericQuestionDialog = {
    dialog: {
        id: "numeric-question-modal"
    },

    label: {
        id: "numeric-question-modal-label"
    },

    questionText: {
        label: {
            id: "numeric-question-modal-question-text-label"
        },
        input: {
            id: "numeric-question-modal-question-text-input"
        }
    },

    explainer: {
        label: {
            id: "numeric-question-modal-explainer-label"
        },
        input: {
            id: "numeric-question-modal-explainer-input"
        }
    },

    variableName: {
        label: {
            id: "numeric-question-modal-variable-name-label"
        },
        input: {
            id: "numeric-question-modal-variable-name-input"
        }
    },

    isMandatory: {
        label: {
            id: "numeric-question-modal-mandatory-label"
        },
        input: {
            id: "numeric-question-modal-mandatory-input"
        }
    },

    isInteger: {
        label: {
            id: "numeric-question-modal-is-integer-label"
        },
        input: {
            id: "numeric-question-modal-is-integer-input"
        }
    },

    minimumValue: {
        label: {
            id: "numeric-question-modal-min-label"
        },
        input: {
            id: "numeric-question-modal-min-input"
        }
    },

    maximumValue: {
        label: {
            id: "numeric-question-modal-max-label"
        },
        input: {
            id: "numeric-question-modal-max-input"
        }
    }
};

const multipleChoiceQuestionDialog = {
    dialog: {
        id: "multichoice-question-modal"
    },

    label: {
        id: "multichoice-question-modal-label"
    },

    questionText: {
        label: {
            id: "multichoice-question-modal-question-text-label"
        },
        input: {
            id: "multichoice-question-modal-question-text-input"
        }
    },

    explainer: {
        label: {
            id: "multichoice-question-modal-explainer-label"
        },
        input: {
            id: "multichoice-question-modal-explainer-input"
        }
    },

    variableName: {
        label: {
            id: "multichoice-question-modal-variable-name-label"
        },
        input: {
            id: "multichoice-question-modal-variable-name-input"
        }
    },

    isMandatory: {
        label: {
            id: "multichoice-question-modal-mandatory-label"
        },
        input: {
            id: "multichoice-question-modal-mandatory-input"
        }
    },

    allowMultiselect: {
        label: {
            id: "multichoice-question-modal-multiselect-label"
        },
        input: {
            id: "multichoice-question-modal-multiselect-input"
        }
    },

    options: {
        label: {
            id: "multichoice-question-modal-options-label"
        },
        table: {
            id: "multichoice-question-modal-options-table"
        },
        optionRow: {
            id: "multichoice-question-modal-options-row",
            textCell: {
                id: "multichoice-question-modal-options-text"
            }
        }
    }
};

/*
 * Question Display Constants
 */
const questionDisplayContainer = {
    id: "questions-display-container"
};

const booleanQuestionDisplay = {
    card: {
        id: "boolean-question-display-card"
    },
    questionText: {
        id: "boolean-question-display-text"
    },
    variableName: {
        id: "boolean-question-display-variable-name"
    },
    explainer: {
        id: "boolean-question-display-explainer"
    },
    isMandatory: {
        id: "boolean-question-display-mandatory"
    }
};

const numericQuestionDisplay = {
    card: {
        id: "numeric-question-display-card"
    },
    questionText: {
        id: "numeric-question-display-text"
    },
    variableName: {
        id: "numeric-question-display-variable-name"
    },
    explainer: {
        id: "numeric-question-display-explainer"
    },
    isMandatory: {
        id: "numeric-question-display-mandatory"
    },
    validationRuleSummary: {
        id: "numeric-question-display-validation-rule-summary"
    }
};

const multipleChoiceQuestionDisplay = {
    card: {
        id: "multichoice-question-display-card"
    },
    questionText: {
        id: "multichoice-question-display-text"
    },
    variableName: {
        id: "multichoice-question-display-variable-name"
    },
    explainer: {
        id: "multichoice-question-display-explainer"
    },
    isMandatory: {
        id: "multichoice-question-display-mandatory"
    },
    isMultiselect: {
        id: "multichoice-question-display-multiselect"
    }
};

/*
 * Rule Dialog Constants
 */
const rulesetDialog = {
    dialog: {
        id: "ruleset-modal"
    },

    label: {
        id: "ruleset-modal-label"
    },

    taxCategory: {
        label: {
            id: "ruleset-modal-tax-category-label"
        },

        input: {
            id: "ruleset-modal-tax-category-input"
        }
    }
};

const ruleTypeDialog = {
    dialog: {
        id: "rule-type-modal"
    },

    label: {
        id: "rule-type-modal-label"
    },

    ruleType: {
        label: {
            id: "rule-type-modal-input-label"
        },

        input: {
            id: "rule-type-modal-input"
        }
    }
};

const flatRateRuleDialog = {
    dialog: {
        id: "flat-rate-rule-modal"
    },

    label: {
        id: "flat-rate-rule-modal-label"
    },

    name: {
        label: {
            id: "flat-rate-rule-modal-name-label"
        },
        input: {
            id: "flat-rate-rule-modal-name-input"
        }
    },

    explainer: {
        label: {
            id: "flat-rate-rule-modal-explainer-label"
        },
        input: {
            id: "flat-rate-rule-modal-explainer-input"
        }
    },

    variableName: {
        label: {
            id: "flat-rate-rule-modal-variable-name-label"
        },
        input: {
            id: "flat-rate-rule-modal-variable-name-input"
        }
    },

    taxRate: {
        label: {
            id: "flat-rate-rule-modal-tax-rate-label"
        },
        input: {
            id: "flat-rate-rule-modal-tax-rate-input"
        }
    }
};

const tieredRateRuleDialog = {
    dialog: {
        id: "tiered-rate-rule-modal"
    },

    label: {
        id: "tiered-rate-rule-modal-label"
    },

    name: {
        label: {
            id: "tiered-rate-rule-modal-name-label"
        },
        input: {
            id: "tiered-rate-rule-modal-name-input"
        }
    },

    explainer: {
        label: {
            id: "tiered-rate-rule-modal-explainer-label"
        },
        input: {
            id: "tiered-rate-rule-modal-explainer-input"
        }
    },

    variableName: {
        label: {
            id: "tiered-rate-rule-modal-variable-name-label"
        },
        input: {
            id: "tiered-rate-rule-modal-variable-name-input"
        }
    },

    tiers: {
        label: {
            id: "tiered-rate-rule-modal-tiers-label"
        },
        table: {
            id: "tiered-rate-rule-modal-tiers-table"
        },
        tierRow: {
            id: "tiered-rate-rule-modal-tiers-row",
            lowerLimit: {
                cellId: "tiered-rate-rule-modal-tiers-min"
            },
            upperLimit: {
                cellId: "tiered-rate-rule-modal-tiers-max"
            },
            taxRate: {
                cellId: "tiered-rate-rule-modal-tiers-rate"
            }
        }
    }
};

const secondaryTieredRateRuleDialog = {
    dialog: {
        id: "secondary-tiered-rate-rule-modal"
    },

    label: {
        id: "secondary-tiered-rate-rule-modal-label"
    },

    name: {
        label: {
            id: "secondary-tiered-rate-rule-modal-name-label"
        },
        input: {
            id: "secondary-tiered-rate-rule-modal-name-input"
        }
    },

    explainer: {
        label: {
            id: "secondary-tiered-rate-rule-modal-explainer-label"
        },
        input: {
            id: "secondary-tiered-rate-rule-modal-explainer-input"
        }
    },

    variableName: {
        label: {
            id: "secondary-tiered-rate-rule-modal-variable-name-label"
        },
        input: {
            id: "secondary-tiered-rate-rule-modal-variable-name-input"
        }
    },

    primaryRule: {
        label: {
            id: "secondary-tiered-rate-rule-modal-primary-rule-label"
        },
        input: {
            id: "secondary-tiered-rate-rule-modal-primary-rule-input"
        }
    },

    tiers: {
        label: {
            id: "secondary-tiered-rate-rule-modal-tiers-label"
        },
        table: {
            id: "secondary-tiered-rate-rule-modal-tiers-table"
        },
        tierRow: {
            id: "secondary-tiered-rate-rule-modal-tiers-row",
            lowerLimit: {
                cellId: "secondary-tiered-rate-rule-modal-tiers-min"
            },
            upperLimit: {
                cellId: "secondary-tiered-rate-rule-modal-tiers-max"
            },
            taxRate: {
                cellId: "secondary-tiered-rate-rule-modal-tiers-rate"
            }
        }
    }
};

const ruleTierDialog = {
    dialog: {
        id: "rule-tier-modal"
    },

    label: {
        id: "rule-tier-modal-label"
    },

    minimumValue: {
        label: {
            id: "rule-tier-modal-min-label"
        },
        input: {
            id: "rule-tier-modal-min-input"
        }
    },

    maximumValue: {
        label: {
            id: "rule-tier-modal-max-label"
        },
        input: {
            id: "rule-tier-modal-max-input"
        }
    },

    taxRate: {
        label: {
            id: "rule-tier-modal-tax-rate-label"
        },
        input: {
            id: "rule-tier-modal-tax-rate-input"
        }
    }
};

const secondaryRuleTierDialog = {
    dialog: {
        id: "secondary-rule-tier-modal"
    },

    label: {
        id: "secondary-rule-tier-modal-label"
    },

    primaryTier: {
        label: {
            id: "secondary-rule-tier-modal-primary-tier-label"
        },
        input: {
            id: "secondary-rule-tier-modal-primary-tier-input"
        }
    },

    taxRate: {
        label: {
            id: "secondary-rule-tier-modal-tax-rate-label"
        },
        input: {
            id: "secondary-rule-tier-modal-tax-rate-input"
        }
    }
};

/*
 * Rule Display Constants
 */
const rulesetsDisplayContainer = {
    id: "rulesets-display-container"
};

const rulesetDisplay = {
    card: {
        id: "ruleset-display-card"
    },
    name: {
        id: "ruleset-display-card-name"
    },
    taxCategpry: {
        id: "ruleset-display-card-tax-category"
    },
    rules: {
        id: "ruleset-display-card-rules"
    }
};

const flatRateRuleDisplay = {
    card: {
        id: "flat-rate-rule-display-card"
    },
    name: {
        id: "flat-rate-rule-display-card-name"
    },
    variableName: {
        id: "flat-rate-rule-display-card-variable-name"
    },
    explainer: {
        id: "flat-rate-rule-display-card-explainer"
    },
    taxRate: {
        id: "flat-rate-rule-display-card-tax-rate"
    }
};

const tieredRateRuleDisplay = {
    card: {
        id: "tiered-rate-rule-display-card"
    },
    name: {
        id: "tiered-rate-rule-display-card-name"
    },
    variableName: {
        id: "tiered-rate-rule-display-card-variable-name"
    },
    explainer: {
        id: "tiered-rate-rule-display-card-explainer"
    }
};

const secondaryTieredRateRuleDisplay = {
    card: {
        id: "secondary-tiered-rate-rule-display-card"
    },
    name: {
        id: "secondary-tiered-rate-rule-display-card-name"
    },
    variableName: {
        id: "secondary-tiered-rate-rule-display-card-variable-name"
    },
    explainer: {
        id: "secondary-tiered-rate-rule-display-card-explainer"
    },
    primaryRule: {
        id: "secondary-tiered-rate-rule-display-card-primary-rule"
    }
};