/*
 * view_models.js
 * Holds the current state of the config app, providing global access
 * to state data 
 */
let app = {
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
    app.dialogState = {
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

function findPreviousQuestion(question) {
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

function getTieredRateRulesForJurisdiction() {
    return getRulesByTypeForJurisdiction('tiered_rate');
}

function getNextRuleOrdinal() {
    if (app.parentRuleset != null) {
        return app.parentRuleset.rules.length + 1;
    } else {
        return null;
    }
}

function findPreviousRule(ruleset, rule) {
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

function findRuleById(ruleId) {
    let rule = null;

    app.jurisdictionRules.forEach(candidateRule => {
        if (candidateRUle.id == ruleId) {
            rule = candidateRule;
        }
    });

    return rule;
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