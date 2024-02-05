/* jshint esversion: 8 */
/*
 * view_models.js
 * Holds the current state of the config app, providing global access
 * to state data 
 */

if (typeof require !== "undefined") {
    const viewConsts = require("./view_consts");
    dialogStates = viewConsts.dialogStates;
}

/*
 * App State
 * Holds the current state of the application including referential data (questions, rulesets, rules),
 * the entity currently being edited, and any parent entity
 * 
 */
let app = {
    apiHost: {
        protocol: "",
        hostname: ""
    },
    jurisdictions: [],
    taxCategories: [],
    allJurisdictionsForm: null,
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
// Clear the entity currently being acted on (created, updated, deleted)
function clearDialogState() {
    app.dialogState = {
        mode: null,
        entityType: null,
        entity: null
    };
}

// Set the entity currently being acted on (created, updated, deleted)
function setDialogState(mode, entityType, entity) {
    app.dialogState = {
        mode: mode,
        entityType: entityType,
        entity: entity
    };
}

// Set the parent of the entity currently being acted on (created, updated, deleted)
function setParentState(mode, entityType, entity) {
    app.parentState = {
        mode: mode,
        entityType: entityType,
        entity: entity
    };
}

// Clear the parent of the entity currently being acted on (created, updated, deleted)
function clearParentState() {
    app.parentState = {
        mode: null,
        entityType: null,
        entity: null
    };
}

// Move the entity currently being acted on into the parent state
function moveAppStateToParentState() {
    app.parentState = app.dialogState;
    clearDialogState();
}

// Move the entity currently being acted on into the parent state
function moveParentStateToAppState() {
    app.dialogState = app.parentState;
    clearParentState();
}

// Set the ruleset that is the parent of the rule currently being acted on
function setParentRuleset(ruleset) {
    app.parentRuleset = ruleset;
}

// Set the common jurisdiction form - this contains questions that will be displayed for all jurisdictions
function setCommonQuestions(form) {
    app.allJurisdictionsForm = form;
}

// Refresh any entities that are held within the app state after
// refreshing the referential data
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
 * View Model Accessor Methods - Forms
 */
function getForm() {
    return app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]];
}

function getFormId() {
    return getForm().id;
}


/*
 * View Model Accessor Methods - Tax Categories
 */
function getTaxCategoryById(id) {
    let category = null;
    app.taxCategories.forEach(taxCategory => {
        if (taxCategory.tax_category_id == id) {
            category = taxCategory;
        }
    });
    return category;
}

function taxCategoryHasRulesetForJurisdiction(taxCategoryId) {
    let hasRuleset = false;
    app.jurisdictionRules.forEach(ruleset => {
        if (ruleset.tax_category_id == taxCategoryId) {
            hasRuleset = true;
        }
    });
    return hasRuleset;
}

/*
 * View Model Accessor Methods - Questions
 */

// Extract questions from the form
function getQuestions() {
    return app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].questions;
}

function getCommonQuestions() {
    if (app.allJurisdictionsForm == null) {
        return [];
    }
    return app.allJurisdictionsForm.forms[Object.keys(app.allJurisdictionsForm.forms)[0]].questions;
}

function isAllJurisdictionsForm(form) {
    if (form == null) {
        return false;
    }
    try {
        return Object.keys(form.forms)[0] == "1";
    } catch (ex) {
        return false;
    }
}

// Calculate the next question ordinal in the current sequence
function getNextQuestionOrdinal() {
    return getQuestions().length + 1;
}

// Get a question based on its database ID
function findQuestionById(questionId) {
    let question = null;

    getQuestions().forEach(candidateQuestion => {
        if (candidateQuestion.id == questionId) {
            question = candidateQuestion;
        }
    });

    return question;
}

// Extract the list of variable names from current questions
// For now, non-numeric questions are excluded as rules are not able
// currently to support responses from non-numeric questions
function getValidQuestionTextVariableNamePairs(includeOnlyNumeric=true) {
    let questions = getQuestions();
    let commonQuestions = getCommonQuestions();
    let allQuestions = questions.concat(commonQuestions);
    let variables = [];
    allQuestions.forEach(question => {
        if ((includeOnlyNumeric && question.type == "numeric") || !includeOnlyNumeric) {
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

// Check if the variable name provided is a duplicate of the existing variable names
function isDuplicateVariableName(variableName) {
    let isDuplicate = false;
    let existingVariableNames = getValidQuestionTextVariableNamePairs(false);
    existingVariableNames.forEach(candidateVariableName => {
        if (candidateVariableName.variableName == variableName) {
            isDuplicate = true;
        }
    });
    return isDuplicate;
}

// Check if there are any rules whose variable name matches the
// variable name of the specified question
function questionHasDependentRules(questionId) {
    // Get the variable name from the question
    let question = findQuestionById(questionId);
    if (question == null) {
        return null;
    }
    let varName = question.variable_name;

    let hasDependents = false;

    // Check all rules to see if there are any dependents
    app.jurisdictionRules.forEach(ruleset => {
        ruleset.rules.forEach(rule => {
            if (rule.variable_name == varName) {
                hasDependents = true;
            }
        });
    });

    return hasDependents;
}

/*
 * View Model Accessor Methods - Multiple choice options
 */

// Find a multiple choice option based on its ID
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

/*
 * View Model Accessor Methods - Rulesets
 */
function findRulesetById(id) {
    let ruleset = null;
    app.jurisdictionRules.forEach(candidateRuleset => {
        if (candidateRuleset.id == id) {
            ruleset = candidateRuleset;
        }
    });
    return ruleset;
}

/*
 * View Model Accessor Methods - Rules
 */

// Get a rule based on its database ID
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

// Check if there are any secondary tiered rules that have the specified
// tiered rate rule as their primary rule
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

// Find the ruleset to which the specified rule belongs
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

// Get all of the currently-loaded tiered rate rules
function getTieredRateRulesForJurisdiction() {
    return getRulesByTypeForJurisdiction('tiered_rate');
}

// Get all of the currently loaded rules for the specified type
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

/*
 * View Model Accessor Methods - Rule Tiers
 */

// Return a rule tier based on its database ID
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

// Return a secondary rule tier based on its database ID
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

// Check if the any secondary rule tier has the specified rule tier
// as its primary tier
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
 * Ordinal Traversal - Questions
 */

// Find the question that immediately precedes the specified one
// based on ordinals
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

// Find the question that immediately follows the specified one
// based on ordinals
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

// Deleting an entity leaves a gap in the ordinal sequence
// E.g., deleting entity with ordinal = 2 will leave the remaining
// ordinlas 1 and 3
// This procedure resequences ordinals so that the entities
// remain in the same order but with no gaps
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

/*
 * Ordinal Traversal - Rulesets
 */

// Find the next ruleset ordinal in the current sequence for the selected
// jurisdiction
function getNextRulesetOrdinal() {
    return app.jurisdictionRules.length + 1;
}

// Find the ruleset that immediately precedes the specified one
// based on ordinals
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

// Find the ruleset that immediately precedes the specified one
// based on ordinals
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

// Deleting an entity leaves a gap in the ordinal sequence
// E.g., deleting entity with ordinal = 2 will leave the remaining
// ordinlas 1 and 3
// This procedure resequences ordinals so that the entities
// remain in the same order but with no gaps
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

/*
 * Ordinal Traversal - Rules
 */

// Get the next ordinal in the sequence
function getNextRuleOrdinal() {
    if (app.parentRuleset != null) {
        return app.parentRuleset.rules.length + 1;
    } else {
        return null;
    }
}

// Find the rule that immediately precedes the specified one
// based on ordinals
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

// Find the question that immediately follows the specified one
// based on ordinals
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

// Deleting an entity leaves a gap in the ordinal sequence
// E.g., deleting entity with ordinal = 2 will leave the remaining
// ordinlas 1 and 3
// This procedure resequences ordinals so that the entities
// remain in the same order but with no gaps
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

/*
 * Ordinal Traversal - Rule Tiers
 */

// Find the next rule tier based on the current sequence
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

// Find the rule tier that immediately precedes the specified one
// based on ordinals
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

// Find the rule tier that immediately precedes the specified one
// based on ordinals
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

// Deleting an entity leaves a gap in the ordinal sequence
// E.g., deleting entity with ordinal = 2 will leave the remaining
// ordinlas 1 and 3
// This procedure resequences ordinals so that the entities
// remain in the same order but with no gaps
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

/*
 * Exports
 */
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
    isDuplicateVariableName,
    questionHasDependentRules,
    taxCategoryHasRulesetForJurisdiction,
    isAllJurisdictionsForm,
    setCommonQuestions
};