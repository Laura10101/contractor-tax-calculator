/*
 * views.js
 * Provides view functions to render views and react to view actions
 */

/*
 * Ruleset Views
 */
function displayRulesets(data) {
    app.jurisdictionRules = data;
    updateRulesetsDisplay(app.jurisdictionRules);
}

function displayRulesetsLoadError() {
    error("An error occurred while loading rulesets for selected jurisdiction.");
}


/*
 * Forms Views
 */
function displayQuestions(data) {
    app.jurisdictionForm = data;
    updateQuestionDisplay(app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].questions);
}

function displayQuestionsLoadError() {
    error("An error occurred while loading questions for selected jurisdiction.");
}

/*
 * Jurisdiction Views
 */
function jurisdictionSelected() {
    jurisdictionId = getSelectedJurisdictionId();
    getFormForJurisdiction(jurisdictionId, displayQuestions, displayQuestionsLoadError);
    getRulesetsForJurisdiction(jurisdictionId, displayRulesets, displayRulesetsLoadError);
}

function loadJurisdictionSelect(data) {
    app.jurisdictions = data.jurisdictions;
    initJurisdictionsSelect(app.jurisdictions, jurisdictionSelected);
}

function displayJurisdictionLoadError() {
    error("An error occurred while loading jurisdictions.");
}

/*
 * Tax Category Views
 */
function loadTaxCategorySelect(data) {
    app.taxCategories = data;
}

function displayTaxCategoryLoadError() {
    error("An error occurred while loading tax categories.");
}

/*
 * Question Views
 */
function refreshQuestionsDisplay() {
    jurisdictionId = getSelectedJurisdictionId();
    getFormForJurisdiction(jurisdictionId, displayQuestions, displayQuestionsLoadError);
}

function editQuestion(question) {
    switch (question.type) {
        case "boolean":
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.booleanQuestion, question);
                displayEditBooleanQuestionDialog(question);
            break;
        case "numeric":
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.numericQuestion, question);
                displayEditNumericQuestionDialog(question);
            break;
        case "multiple_choice":
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);
                displayEditMultipleChoiceQuestionDialog(question);
            break;
    }
}

function saveQuestionSucceeded() {
    success("The question was successfully saved.");
    refreshQuestionsDisplay();
}

function saveQuestionFailed(request, status, message) {
    error("An error occurred while attempting to save question.");
}

function saveQuestion() {
    formId = app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].id;

    if (app.dialogState.mode == dialogStates.modes.create) {
        
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        question = app.dialogState.entity;

        switch(app.dialogState.entityType) {
            case dialogStates.entityTypes.booleanQuestion:
                break;
            case dialogStates.entityTypes.numericQuestion:
                    hideDialog(numericQuestionDialog.dialog.id);
                    updateNumericQuestion(
                        formId,
                        question.id,
                        document.getElementById(numericQuestionDialog.questionText.input.id).value,
                        question.ordinal,
                        document.getElementById(numericQuestionDialog.explainer.input.id).value,
                        document.getElementById(numericQuestionDialog.isMandatory.input.id).checked,
                        document.getElementById(numericQuestionDialog.isInteger.input.id).checked,
                        document.getElementById(numericQuestionDialog.minimumValue.input.id).value,
                        document.getElementById(numericQuestionDialog.maximumValue.input.id).value,
                        saveQuestionSucceeded,
                        saveQuestionFailed
                    );
                break;
            case dialogStates.entityTypes.multipleChoiceQuestion:
                break;
        }
    } else {
        error("Invalid dialog mode " + app.dialogState.mode + " found when saving question.");
    }
}

function deleteQuestion(question) {
    
}

function moveQuestionUp(question) {

}

function moveQuestionDown(question) {

}

/*
 * Multiple Choice Option Views
 */

/*
 * Flat Rate Rule Views
 */

/*
 * Tiered Rate Rule Views
 */

/*
 * Rule Tier Views
 */

/*
 * Secondary Tiered Rate Rule Views
 */

/*
 * Secondary Rule Tier Views
 */

/*
 * Initialisation functions
 */
function init() {
    getJurisdictions(loadJurisdictionSelect, displayJurisdictionLoadError);
    getTaxCategories(loadTaxCategorySelect, displayTaxCategoryLoadError);
}

window.onload = init();