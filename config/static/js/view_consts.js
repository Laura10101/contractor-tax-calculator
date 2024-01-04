/*
 * view_consts.js
 * Defines constants used to simplify access to key DOM elements and other resources
 */

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
            id: "question-type-modal-input-label"
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

    maxiumValue: {
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
    id: "questionsDisplayContainer"
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
    id: "rulesetsDisplayContainer"
};

const rulesetDisplay = {
    card: {
        id: ""
    },
    name: {
        id: ""
    },
    taxCategpry: {
        id: ""
    },
    rules: {
        id: ""
    }
};

const flatRateRuleDisplay = {
    card: {
        id: ""
    },
    name: {
        id: ""
    },
    variableName: {
        id: ""
    },
    explainer: {
        id: ""
    },
    taxRate: {
        id: ""
    }
};

const tieredRateRuleDisplay = {
    card: {
        id: ""
    },
    name: {
        id: ""
    },
    variableName: {
        id: ""
    },
    explainer: {
        id: ""
    }
};

const secondaryTieredRateRuleDisplay = {
    card: {
        id: ""
    },
    name: {
        id: ""
    },
    variableName: {
        id: ""
    },
    explainer: {
        id: ""
    },
    primaryRule: {
        id: ""
    }
};