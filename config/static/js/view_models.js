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

function setParentRuleset(ruleset) {
    app.parentRuleset = ruleset;
}

function getFormId() {
    return app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].id;
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