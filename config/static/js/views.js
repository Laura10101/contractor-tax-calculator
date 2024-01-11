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
    jurisdictionSelected();
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

function questionTypeSelected() {
    // Hide question type dialog
    hideDialog(questionTypeDialog.dialog.id);

    // Get the question type
    questionType = document.getElementById(questionTypeDialog.questionType.input.id).value;

    // Trigger the appropriate create dialog
    switch(questionType) {
        case "boolean":
                setDialogState(dialogStates.modes.create, dialogStates.entityTypes.booleanQuestion, null);
                displayCreateBooleanQuestionDialog();
            break;
        case "numeric":
                setDialogState(dialogStates.modes.create, dialogStates.entityTypes.numericQuestion, null);
                displayCreateNumericQuestionDialog();
            break;
        case "multiple_choice":
                setDialogState(dialogStates.modes.create, dialogStates.entityTypes.multipleChoiceQuestion, null);
                displayCreateMultipleChoiceQuestionDialog();
            break;
    }
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
    clearDialogState();
    refreshQuestionsDisplay();
}

function saveQuestionFailed(request, status, message) {
    error("An error occurred while attempting to save question.");
}

function saveQuestion() {
    formId = app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].id;

    if (app.dialogState.mode == dialogStates.modes.create) {
        switch (app.dialogState.entityType) {
            // Create boolean question
            case dialogStates.entityTypes.booleanQuestion:
                    hideDialog(booleanQuestionDialog.dialog.id);
                    createBooleanQuestion(
                        formId,
                        document.getElementById(booleanQuestionDialog.questionText.input.id).value,
                        1,
                        document.getElementById(booleanQuestionDialog.explainer.input.id).value,
                        document.getElementById(booleanQuestionDialog.variableName.input.id).value,
                        document.getElementById(booleanQuestionDialog.isMandatory.input.id).checked,
                        saveQuestionSucceeded,
                        saveQuestionFailed
                    );
                break;
            // Create numeric question
            case dialogStates.entityTypes.numericQuestion:
                    hideDialog(numericQuestionDialog.dialog.id);
                    createNumericQuestion(
                        formId,
                        document.getElementById(numericQuestionDialog.questionText.input.id).value,
                        1,
                        document.getElementById(numericQuestionDialog.explainer.input.id).value,
                        document.getElementById(numericQuestionDialog.variableName.input.id).value,
                        document.getElementById(numericQuestionDialog.isMandatory.input.id).checked,
                        document.getElementById(numericQuestionDialog.isInteger.input.id).checked,
                        document.getElementById(numericQuestionDialog.minimumValue.input.id).value,
                        document.getElementById(numericQuestionDialog.maximumValue.input.id).value,
                        saveQuestionSucceeded,
                        saveQuestionFailed
                    )
                break;
            // Create multiple choice questions
            case dialogStates.entityTypes.multipleChoiceQuestion:
                    hideDialog(multipleChoiceQuestionDialog.dialog.id);
                    createMultipleChoiceQuestion(
                        formId,
                        document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value,
                        1,
                        document.getElementById(multipleChoiceQuestionDialog.explainer.input.id).value,
                        document.getElementById(multipleChoiceQuestionDialog.variableName.input.id).value,
                        document.getElementById(multipleChoiceQuestionDialog.isMandatory.input.id).checked,
                        saveQuestionSucceeded,
                        saveQuestionFailed
                    )
                break;
        }
        
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        question = app.dialogState.entity;

        switch(app.dialogState.entityType) {
            // Edit boolean question
            case dialogStates.entityTypes.booleanQuestion:
                    hideDialog(booleanQuestionDialog.dialog.id);
                    updateBooleanQuestion(
                        formId,
                        question.id,
                        document.getElementById(booleanQuestionDialog.questionText.input.id).value,
                        question.ordinal,
                        document.getElementById(booleanQuestionDialog.explainer.input.id).value,
                        document.getElementById(booleanQuestionDialog.isMandatory.input.id).checked,
                        saveQuestionSucceeded,
                        saveQuestionFailed
                    )
                break;
            // Edit numeric question
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
            // Edit multiple choice question
            case dialogStates.entityTypes.multipleChoiceQuestion:
                    hideDialog(multipleChoiceQuestionDialog.dialog.id);
                    updateMultipleChoiceQuestion(
                        formId,
                        question.id,
                        document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value,
                        question.ordinal,
                        document.getElementById(multipleChoiceQuestionDialog.explainer.input.id).value,
                        document.getElementById(multipleChoiceQuestionDialog.isMandatory.input.id).checked,
                        saveQuestionSucceeded,
                        saveQuestionFailed
                    )
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