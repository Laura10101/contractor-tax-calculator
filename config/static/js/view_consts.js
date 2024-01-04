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
        id: ""
    },
    questionText: {
        id: ""
    },
    variableName: {
        id: ""
    },
    explainer: {
        id: ""
    },
    isMandatory: {
        id: ""
    }
};

const numericQuestionDisplay = {
    card: {
        id: ""
    },
    questionText: {
        id: ""
    },
    variableName: {
        id: ""
    },
    explainer: {
        id: ""
    },
    isMandatory: {
        id: ""
    },
    validRuleSummary: {
        id: ""
    }
};

const multipleChoiceQuestionDisplay = {
    card: {
        id: ""
    },
    questionText: {
        id: ""
    },
    variableName: {
        id: ""
    },
    explainer: {
        id: ""
    },
    isMandatory: {
        id: ""
    },
    isMultiselect: {
        id: ""
    }
};

/*
 * Rule Dialog Constants
 */
const rulesetDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    taxCategory: {
        label: {
            id: ""
        },

        input: {
            id: ""
        }
    }
};

const ruleTypeDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    ruleType: {
        label: {
            id: ""
        },

        input: {
            id: ""
        }
    }
};

const flatRateRuleDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    name: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    explainer: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    variableName: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    taxRate: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    }
};

const tieredRateRuleDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    name: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    explainer: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    variableName: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    tiers: {
        label: {
            id: ""
        },
        table: {
            id: ""
        },
        tierRow: {
            id: "",
            lowerLimit: {
                cellId: ""
            },
            upperLimit: {
                cellId: ""
            },
            taxRate: {
                cellId: ""
            }
        }
    }
};

const secondaryTieredRateRuleDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    name: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    explainer: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    variableName: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    primaryRule: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    tiers: {
        label: {
            id: ""
        },
        table: {
            id: ""
        },
        tierRow: {
            id: "",
            lowerLimit: {
                cellId: ""
            },
            upperLimit: {
                cellId: ""
            },
            taxRate: {
                cellId: ""
            }
        }
    }
};

const ruleTierDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    minimumValue: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    maximumValue: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    taxRate: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    }
};

const secondaryRuleTierDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    primaryTier: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    taxRate: {
        label: {
            id: ""
        },
        input: {
            id: ""
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