/* jshint esversion: 8 */

if (typeof require !== "undefined") {
    const viewConsts = require("./view_consts");
    dialogStates = viewConsts.dialogStates;
}

/*
 * view_models.js
 * Holds the current state of the config app, providing global access
 * to state data 
 */
let app = {
    apiHost: {
        protocol: "",
        hostname: ""
    },
    jurisdictions: [],
    taxCategories: [],
    jurisdictionForm: {},
    jurisdictionRules: [],
    dialogState: {
        mode: null,
        entityType: null,
        entity: null
    },
    parentState: {
        mode: null,
        entityType: null,
        entity: null
    },
    parentRuleset: null
}

/*
 * API Host View Model Methods
 */
function setApiHost(protocol, hostname) {
    app.apiHost.protocol = protocol;
    app.apiHost.hostname = hostname;
}

/*
 * State Management View Model Methods
 */
function clearDialogState() {
    app.dialogState = {
        mode: null,
        entityType: null,
        entity: null
    };
    app.parentRuleset = null
}

function setDialogState(mode, entityType, entity) {
    app.dialogState = {
        mode: mode,
        entityType: entityType,
        entity: entity
    };
}

function setParentState(mode, entityType, entity) {
    app.parentState = {
        mode: mode,
        entityType: entityType,
        entity: entity
    };
}

function clearParentState() {
    app.parentState = {
        mode: null,
        entityType: null,
        entity: null
    };
}

function moveAppStateToParentState() {
    app.parentState = app.dialogState;
    clearDialogState();
}

function moveParentStateToAppState() {
    app.dialogState = app.parentState;
    clearParentState();
}

function setParentRuleset(ruleset) {
    app.parentRuleset = ruleset;
}

// Refresh any entities that are held within the app state after
// refreshing the 
function refreshAppState() {
    // Update parent ruleset
    if (app.parentRuleset != null) {
        setParentRuleset(findRulesetById(app.parentRuleset.id));
    }

    // Update dialog state
    if (app.dialogState.entity != null) {
        switch (app.dialogState.entityType) {
            case dialogStates.entityTypes.booleanQuestion:
                    app.dialogState.entity = findQuestionById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.numericQuestion:
                    app.dialogState.entity = findQuestionById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.multipleChoiceQuestion:
                    app.dialogState.entity = findQuestionById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.question:
                    app.dialogState.entity = findQuestionById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.multipleChoiceOption:
                    app.dialogState.entity = findMultiplpeChoiceOptionById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.ruleset:
                    app.dialogState.entity = findRulesetById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.flatRateRule:
                    app.dialogState.entity = findRuleById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.tieredRateRule:
                    app.dialogState.entity = findRuleById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.secondaryTieredRateRule:
                    app.dialogState.entity = findRuleById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.rule:
                    app.dialogState.entity = findRuleById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.ruleTier:
                    app.dialogState.entity = findPrimaryRuleTierById(app.dialogState.entity.id);
                break;
            case dialogStates.entityTypes.secondaryRuleTier:
                    app.dialogState.entity = findSecondaryRuleTierById(app.dialogState.entity.id);
                break;
        }
    }

    // Update parent state
    if (app.parentState.entity != null) {
        switch (app.parentState.entityType) {
            case dialogStates.entityTypes.booleanQuestion:
                    app.parentState.entity = findQuestionById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.numericQuestion:
                    app.parentState.entity = findQuestionById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.multipleChoiceQuestion:
                    app.parentState.entity = findQuestionById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.question:
                    app.parentState.entity = findQuestionById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.multipleChoiceOption:
                    app.parentState.entity = findMultiplpeChoiceOptionById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.ruleset:
                    app.parentState.entity = findRulesetById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.flatRateRule:
                    app.parentState.entity = findRuleById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.tieredRateRule:
                    app.parentState.entity = findRuleById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.secondaryTieredRateRule:
                    app.parentState.entity = findRuleById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.rule:
                    app.parentState.entity = findRuleById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.ruleTier:
                    app.parentState.entity = findPrimaryRuleTierById(app.parentState.entity.id);
                break;
            case dialogStates.entityTypes.secondaryRuleTier:
                    app.parentState.entity = findSecondaryRuleTierById(app.parentState.entity.id);
                break;
        }
    }
}

/*
 * View Model Accessor Methods
 */
function getForm() {
    return app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]];
}

function getFormId() {
    return getForm().id;
}

function getTaxCategoryById(id) {
    let category = null;
    app.taxCategories.forEach(taxCategory => {
        if (taxCategory.tax_category_id == id) {
            category = taxCategory;
        }
    });
    return category;
}

function getQuestions() {
    return app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].questions;
}

function getNextQuestionOrdinal() {
    return getQuestions().length + 1;
}

function findQuestionById(questionId) {
    let question = null;

    getQuestions().forEach(candidateQuestion => {
        if (candidateQuestion.id == questionId) {
            question = candidateQuestion;
        }
    });

    return question;
}

function getValidQuestionTextVariableNamePairs() {
    let questions = getQuestions();
    let variables = [];
    questions.forEach(question => {
        if (question.type == "numeric") {
            variables.push({
                questionText: question.text,
                variableName: question.variable_name
            });
        }
    });
    return variables.sort(function(a, b) {
        if (a.variableName == b.variableName) {
            return 0;
        }

        return a.variableName < b.variableName ? -1 : 1;
    });
}

function isDuplicateVariableName(variableName) {
    let isDuplicate = false;
    let existingVariableNames = getValidQuestionTextVariableNamePairs();
    existingVariableNames.forEach(candidateVariableName => {
        if (candidateVariableName.variableName == variableName) {
            isDuplicate = true;
        }
    });
    return isDuplicate;
}

function findMultiplpeChoiceOptionById(optionId) {
    let option = null;

    getQuestions().forEach(candidateQuestion => {
        if (candidateQuestion.type == "multiple_choice") {
            question.options.forEach(candidateOption => {
                if (candidateOption.id == optionId) {
                    option = candidateOption;
                }
            });
        }
    });

    return option;
}

function findRulesetById(id) {
    let ruleset = null;
    app.jurisdictionRules.forEach(candidateRuleset => {
        if (candidateRuleset.id == id) {
            ruleset = candidateRuleset;
        }
    });
    return ruleset;
}

function getTieredRateRulesForJurisdiction() {
    return getRulesByTypeForJurisdiction('tiered_rate');
}

function findRuleById(ruleId) {
    let rule = null;

    app.jurisdictionRules.forEach(candidateRuleset => {
        candidateRuleset.rules.forEach(candidateRule => {
            if (candidateRule.id == ruleId) {
                rule = candidateRule;
            }
        }); 
    });

    return rule;
}

function primaryRuleHasDependentSecondaryRules(primaryRuleId) {
    let hasDependents = false;
    let primaryRule = findRuleById(primaryRuleId);
    if (primaryRule == null) {
        return null;
    }
    let secondaryRules = getRulesByTypeForJurisdiction("secondary_tiered_rate");
    secondaryRules.forEach(secondaryRule => {
        if (secondaryRule.primary_rule_id == primaryRuleId) {
            hasDependents = true;
        }
    });
    return hasDependents;
}

function findParentRuleset(ruleId) {
    let ruleset = null;

    app.jurisdictionRules.forEach(candidateRuleset => {
        candidateRuleset.rules.forEach(candidateRule => {
            if (candidateRule.id == ruleId) {
                ruleset = candidateRuleset;
            }
        });
    });

    return ruleset;
}

function findPrimaryRuleTierById(tierId) {
    let tier = null;

    app.jurisdictionRules.forEach(candidateRuleset => {
        candidateRuleset.rules.forEach(candidateRule => {
            if (candidateRule.type == "tiered_rate") {
                candidateRule.tiers.forEach(candidateTier => {
                    if (candidateTier.id == tierId) {
                        tier = candidateTier;
                    }
                });
            }
        });
    });

    return tier;
}

function findSecondaryRuleTierById(tierId) {
    let tier = null;

    app.jurisdictionRules.forEach(candidateRuleset => {
        candidateRuleset.rules.forEach(candidateRule => {
            if (candidateRule.type == "secondary_tiered_rate") {
                candidateRule.tiers.forEach(candidateTier => {
                    if (candidateTier.id == tierId) {
                        tier = candidateTier;
                    }
                });
            }
        });
    });

    return tier;
}

function primaryRuleTierHasDependentSecondaryTiers(primaryTierId) {
    let hasDependents = false;
    let primaryTier = findPrimaryRuleTierById(primaryTierId);
    if (primaryTier == null) {
        return null;
    }
    let secondaryRules = getRulesByTypeForJurisdiction("secondary_tiered_rate");
    secondaryRules.forEach(secondaryRule => {
        secondaryRule.tiers.forEach(secondaryTier => {
            if (secondaryTier.primary_tier_id == primaryTierId) {
                hasDependents = true;
            }
        });
    });
    return hasDependents;
}

/*
 * Ordinal Traversal
 */
function findPreviousQuestion(question) {
    if (question == null || question.ordinal == null) {
        return null;
    }
    
    let questions = getQuestions();
    let previousQuestion = null;
    questions.forEach(candidateQuestion => {
        if (candidateQuestion.id != question.id) {
            if (previousQuestion == null) {
                if (candidateQuestion.ordinal < question.ordinal) {
                    previousQuestion = candidateQuestion;
                }
            } else {
                if (candidateQuestion.ordinal > previousQuestion.ordinal && candidateQuestion.ordinal < question.ordinal) {
                    previousQuestion = candidateQuestion;
                }
            }
        }
    });
    return previousQuestion;
}

function findNextQuestion(question) {
    if (question == null || question.ordinal == null) {
        return null;
    }

    let questions = getQuestions();
    let nextQuestion = null;
    questions.forEach(candidateQuestion => {
        if (candidateQuestion.id != question.id) {
            if (nextQuestion == null) {
                if (candidateQuestion.ordinal > question.ordinal) {
                    nextQuestion = candidateQuestion;
                }
            } else {
                if (candidateQuestion.ordinal < nextQuestion.ordinal && candidateQuestion.ordinal > question.ordinal) {
                    nextQuestion = candidateQuestion;
                }
            }
        }
    });
    return nextQuestion;
}

function resequenceQuestionOrdinals(deletedQuestion) {
    let questions = getQuestions();
    let i = 0;
    questions.forEach(question => {
        if (question.id != deletedQuestion.id) {
            i++;
            question.ordinal = i;
        }
    });
    return questions;
}

function getNextRulesetOrdinal() {
    return app.jurisdictionRules.length + 1;
}

function findPreviousRuleset(ruleset) {
    if (ruleset == null || ruleset.ordinal == null) {
        return null;
    }

    let rulesets = app.jurisdictionRules;
    let previousRuleset = null;
    rulesets.forEach(candidateRuleset => {
        if (candidateRuleset.id != ruleset.id) {
            if (previousRuleset == null) {
                if (candidateRuleset.ordinal < ruleset.ordinal) {
                    previousRuleset = candidateRuleset;
                }
            } else {
                if (candidateRuleset.ordinal > previousRuleset.ordinal && candidateRuleset.ordinal < ruleset.ordinal) {
                    previousRuleset = candidateRuleset;
                }
            }
        }
    });
    return previousRuleset;
}

function findNextRuleset(ruleset) {
    if (ruleset == null || ruleset.ordinal == null) {
        return null;
    }

    let rulesets = app.jurisdictionRules;
    let nextRuleset = null;
    rulesets.forEach(candidateRuleset => {
        if (candidateRuleset.id != ruleset.id) {
            if (nextRuleset == null) {
                if (candidateRuleset.ordinal > ruleset.ordinal) {
                    nextRuleset = candidateRuleset;
                }
            } else {
                if (candidateRuleset.ordinal < nextRuleset.ordinal && candidateRuleset.ordinal > ruleset.ordinal) {
                    nextRuleset = candidateRuleset;
                }
            }
        }
    });
    return nextRuleset;
}

function resequenceRulesetOrdinals(deletedRuleset) {
    let rulesets = app.jurisdictionRules;
    let i = 0;
    rulesets.forEach(ruleset => {
        if (ruleset.id != deletedRuleset.id) {
            i++;
            ruleset.ordinal = i;
        }
    });
    return rulesets;
}

function getRulesByTypeForJurisdiction(type) {
    rules = [];
    app.jurisdictionRules.forEach(ruleset => {
        ruleset.rules.forEach(rule => {
            if (rule.type == type) {
                rules.push(rule);
            }
        });
    });
    return rules;
}

function getNextRuleOrdinal() {
    if (app.parentRuleset != null) {
        return app.parentRuleset.rules.length + 1;
    } else {
        return null;
    }
}

function findPreviousRule(ruleset, rule) {
    if (ruleset == null || rule == null || ruleset.rules == null || rule.ordinal == null) {
        return null;
    }

    let rules = ruleset.rules;
    let previousRule = null;
    rules.forEach(candidateRule => {
        if (candidateRule.id != rule.id) {
            if (previousRule == null) {
                if (candidateRule.ordinal < rule.ordinal) {
                    previousRule = candidateRule;
                }
            } else {
                if (candidateRule.ordinal > previousRule.ordinal && candidateRule.ordinal < rule.ordinal) {
                    previousRule = candidateRule;
                }
            }
        }
    });
    return previousRule;
}

function findNextRule(ruleset, rule) {
    if (ruleset == null || rule == null || ruleset.rules == null || rule.ordinal == null) {
        return null;
    }

    let rules = ruleset.rules;
    let nextRule = null;
    rules.forEach(candidateRule => {
        if (candidateRule.id != rule.id) {
            if (nextRule == null) {
                if (candidateRule.ordinal > rule.ordinal) {
                    nextRule = candidateRule;
                }
            } else {
                if (candidateRule.ordinal < nextRule.ordinal && candidateRule.ordinal > rule.ordinal) {
                    nextRule = candidateRule;
                }
            }
        }
    });
    return nextRule;
}

function resequenceRuleOrdinals(deletedRule) {
    let rules = app.parentRuleset.rules;
    let i = 0;
    rules.forEach(rule => {
        if (rule.id != deletedRule.id) {
            i++;
            rule.ordinal = i;
        }
    });
    return rules;
}

function getNextRuleTierOrdinal(rule) {
    if (rule != null) {
        if (rule.type == "tiered_rate" || rule.type == "secondary_tiered_rate") {
            return rule.tiers.length + 1;
        } else {
            return null;
        }
    } else {
        return null;
    }
}

function findPreviousRuleTier(rule, tier) {
    if (rule == null || tier == null || rule.tiers == null || tier.ordinal == null) {
        return null;
    }
    let tiers = rule.tiers;
    let previousTier = null;
    tiers.forEach(candidateTier => {
        if (candidateTier.id != tier.id) {
            if (previousTier == null) {
                if (candidateTier.ordinal < tier.ordinal) {
                    previousTier = candidateTier;
                }
            } else {
                if (candidateTier.ordinal > previousTier.ordinal && candidateTier.ordinal < tier.ordinal) {
                    previousTier = candidateTier;
                }
            }
        }
    });
    return previousTier;
}

function findNextRuleTier(rule, tier) {
    if (rule == null || tier == null || rule.tiers == null || tier.ordinal == null) {
        return null;
    }

    let tiers = rule.tiers;
    let nextTier = null;
    tiers.forEach(candidateTier => {
        if (candidateTier.id != tier.id) {
            if (nextTier == null) {
                if (candidateTier.ordinal > tier.ordinal) {
                    nextTier = candidateTier;
                }
            } else {
                if (candidateTier.ordinal < nextTier.ordinal && candidateTier.ordinal > tier.ordinal) {
                    nextTier = candidateTier;
                }
            }
        }
    });
    return nextTier;
}

function resequenceRuleTierOrdinals(deletedTier) {
    let tiers = app.parentState.entity.tiers;
    let i = 0;
    tiers.forEach(tier => {
        if (tier.id != deletedTier.id) {
            i++;
            tier.ordinal = i;
        }
    });
    return tiers;
}

if (typeof module !== "undefined") module.exports = {
    app,
    clearDialogState,
    setDialogState,
    setParentState,
    clearParentState,
    moveAppStateToParentState,
    moveParentStateToAppState,
    setParentRuleset,
    getForm,
    getFormId,
    getTaxCategoryById,
    getQuestions,
    getNextQuestionOrdinal,
    findQuestionById,
    getTieredRateRulesForJurisdiction,
    findRuleById,
    findParentRuleset,
    findPrimaryRuleTierById,
    findPreviousQuestion,
    findNextQuestion,
    resequenceQuestionOrdinals,
    getNextRulesetOrdinal,
    findPreviousRuleset,
    findNextRuleset,
    resequenceRulesetOrdinals,
    getRulesByTypeForJurisdiction,
    getNextRuleOrdinal,
    findPreviousRule,
    findNextRule,
    resequenceRuleOrdinals,
    getNextRuleTierOrdinal,
    findPreviousRuleTier,
    findNextRuleTier,
    resequenceRuleTierOrdinals,
    refreshAppState,
    primaryRuleHasDependentSecondaryRules,
    primaryRuleTierHasDependentSecondaryTiers,
    getValidQuestionTextVariableNamePairs,
    isDuplicateVariableName
};