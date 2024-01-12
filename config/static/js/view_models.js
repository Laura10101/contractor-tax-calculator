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
    }
}

function clearDialogState() {
    app.dialogState = {

    };
}

function setDialogState(mode, entityType, entity) {
    app.dialogState = {
        mode: mode,
        entityType: entityType,
        entity: entity
    };
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