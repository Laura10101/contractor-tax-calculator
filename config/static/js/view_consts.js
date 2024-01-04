/*
 * view_consts.js
 * Defines constants used to simplify access to key DOM elements and other resources
 */

/*
 * Question Dialog Constants
 */
questionTypeDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    questionType: {
        label: {
            id: ""
        },

        input: {
            id: ""
        }
    }
};

booleanQuestionDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    questionText: {
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

    isMandatory: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    }
};

numericQuestionDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    questionText: {
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

    isMandatory: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    isInteger: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    minimumValue: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    maxiumValue: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    }
};

multipleChoiceQuestionDialog = {
    dialog: {
        id: ""
    },

    label: {
        id: ""
    },

    questionText: {
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

    isMandatory: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    allowMultiselect: {
        label: {
            id: ""
        },
        input: {
            id: ""
        }
    },

    options: {
        label: {
            id: ""
        },
        table: {
            id: ""
        },
        optionRow: {
            id: "",
            textCell: {
                id: ""
            }
        }
    }
};

/*
 * Question Display Constants
 */
questionDisplayContainer = {
    id: ""
};

booleanQuestionDisplay = {
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

numericQuestionDisplay = {
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

multipleChoiceQuestionDisplay = {
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
rulesetDialog = {
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

ruleTypeDialog = {
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

flatRateRuleDialog = {
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

tieredRateRuleDialog = {
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

secondaryTieredRateRuleDialog = {
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

ruleTierDialog = {
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

secondaryRuleTierDialog = {
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
rulesetDisplayContainer = {
    id: ""
};

rulesetDisplay = {
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

flatRateRuleDisplay = {
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

tieredRateRuleDisplay = {
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

secondaryTieredRateRuleDisplay = {
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