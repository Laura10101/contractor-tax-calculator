/* jshint esversion: 8 */
/*
 * views.js
 * Provides view functions to render views and react to view actions
 */
if (typeof require !== "undefined") {
    const viewConsts = require("./view_consts.js");
    const serviceClients = require("./service_clients.js");
    const viewModels = require("./view_models.js");
    const viewUtils = require("./view_utils.js");

    // View consts
    dialogStates = viewConsts.dialogStates;
    confirmationDialog = viewConsts.confirmationDialog;
    questionTypeDialog = viewConsts.questionTypeDialog;
    booleanQuestionDialog = viewConsts.booleanQuestionDialog;
    numericQuestionDialog = viewConsts.numericQuestionDialog;
    multipleChoiceQuestionDialog = viewConsts.multipleChoiceQuestionDialog;
    multipleChoiceOptionDialog = viewConsts.multipleChoiceOptionDialog;
    rulesetDialog = viewConsts.rulesetDialog;
    ruleTypeDialog = viewConsts.ruleTypeDialog;
    flatRateRuleDialog = viewConsts.flatRateRuleDialog;
    tieredRateRuleDialog = viewConsts.tieredRateRuleDialog;
    secondaryTieredRateRuleDialog = viewConsts.secondaryTieredRateRuleDialog;
    ruleTierDialog = viewConsts.ruleTierDialog;
    secondaryRuleTierDialog = viewConsts.secondaryRuleTierDialog;

    // Service clients
    getJurisdictions = serviceClients.getJurisdictions;
    getTaxCategories = serviceClients.getTaxCategories;
    getFormForJurisdiction = serviceClients.getFormForJurisdiction;
    createBooleanQuestion = serviceClients.createBooleanQuestion;
    updateBooleanQuestion = serviceClients.updateBooleanQuestion;
    createNumericQuestion = serviceClients.createNumericQuestion;
    updateNumericQuestion = serviceClients.updateNumericQuestion;
    createMultipleChoiceQuestion = serviceClients.createMultipleChoiceQuestion;
    updateMultipleChoiceQuestion = serviceClients.updateMultipleChoiceQuestion;
    updateQuestion = serviceClients.updateQuestion;
    removeQuestion = serviceClients.removeQuestion;
    postMultipleChoiceOption = serviceClients.postMultipleChoiceOption;
    removeMultipleChoiceOption = serviceClients.removeMultipleChoiceOption;
    getRulesetsForJurisdiction = serviceClients.getRulesetsForJurisdiction;
    postRuleset = serviceClients.postRuleset;
    patchRuleset = serviceClients.patchRuleset;
    removeRuleset = serviceClients.removeRuleset;
    createFlatRateRule = serviceClients.createFlatRateRule;
    updateFlatRateRule = serviceClients.updateFlatRateRule;
    createTieredRateRule = serviceClients.createTieredRateRule;
    updateTieredRateRule = serviceClients.updateTieredRateRule;
    createSecondaryTieredRateRule = serviceClients.createSecondaryTieredRateRule;
    updateSecondaryTieredRateRule = serviceClients.updateSecondaryTieredRateRule;
    removeRule = serviceClients.removeRule;
    postRuleTier = serviceClients.postRuleTier;
    updateRuleTier = serviceClients.updateRuleTier;
    removeRuleTier = serviceClients.removeRuleTier;
    postSecondaryRuleTier = serviceClients.postSecondaryRuleTier;
    updateSecondaryRuleTier = serviceClients.updateSecondaryRuleTier;
    removeSecondaryRuleTier = serviceClients.removeSecondaryRuleTier;
    processBatch = serviceClients.processBatch;
    updateRule = serviceClients.updateRule;

    // View models
    app = viewModels.app;
    getFormId = viewModels.getFormId;
    findQuestionById = viewModels.findQuestionById;
    findRuleById = viewModels.findRuleById;
    findParentRuleset = viewModels.findParentRuleset;
    moveAppStateToParentState = viewModels.moveAppStateToParentState;
    moveParentStateToAppState = viewModels.moveParentStateToAppState;
    clearDialogState = viewModels.clearDialogState;
    clearParentState = viewModels.clearParentState;
    setDialogState = viewModels.setDialogState;
    setParentState = viewModels.setParentState;
    setParentRuleset = viewModels.setParentRuleset;
    getTieredRateRulesForJurisdiction = viewModels.getTieredRateRulesForJurisdiction;
    resequenceQuestionOrdinals = viewModels.resequenceQuestionOrdinals;
    resequenceRuleOrdinals = viewModels.resequenceRuleOrdinals;
    resequenceRulesetOrdinals = viewModels.resequenceRulesetOrdinals;
    resequenceRuleTierOrdinals = viewModels.resequenceRuleTierOrdinals;
    findNextQuestion = viewModels.findNextQuestion;
    findPreviousQuestion = viewModels.findPreviousQuestion;
    findNextRuleset = viewModels.findNextRuleset;
    findPreviousRuleset = viewModels.findPreviousRuleset;
    findNextRule = viewModels.findNextRule;
    findPreviousRule = viewModels.findPreviousRule;
    findNextRuleTier = viewModels.findNextRuleTier;
    findPreviousRuleTier = viewModels.findPreviousRuleTier;
    getNextQuestionOrdinal = viewModels.getNextQuestionOrdinal;
    getNextRulesetOrdinal = viewModels.getNextRulesetOrdinal;
    getNextRuleOrdinal = viewModels.getNextRuleOrdinal;
    getNextRuleTierOrdinal = viewModels.getNextRuleTierOrdinal;
    refreshAppState = viewModels.refreshAppState;
    primaryRuleHasDependentSecondaryRules = viewModels.primaryRuleHasDependentSecondaryRules;
    primaryRuleTierHasDependentSecondaryTiers = viewModels.primaryRuleTierHasDependentSecondaryTiers;
    getValidQuestionTextVariableNamePairs = viewModels.getValidQuestionTextVariableNamePairs;
    isDuplicateVariableName = viewModels.isDuplicateVariableName;
    questionHasDependentRules = viewModels.questionHasDependentRules;
    isAllJurisdictionsForm = viewModels.isAllJurisdictionsForm;
    setCommonQuestions = viewModels.setCommonQuestions;

    // View utils
    showDialog = viewUtils.showDialog;
    hideDialog = viewUtils.hideDialog;
    error = viewUtils.error;
    success = viewUtils.success;
    confirm = viewUtils.confirm;
    updateRuleTierTable = viewUtils.updateRuleTierTable;
    initJurisdictionsSelect = viewUtils.initJurisdictionsSelect;
    getSelectedJurisdictionId = viewUtils.getSelectedJurisdictionId;
    displayCreateBooleanQuestionDialog = viewUtils.displayCreateBooleanQuestionDialog;
    displayEditBooleanQuestionDialog = viewUtils.displayEditBooleanQuestionDialog;
    displayCreateNumericQuestionDialog = viewUtils.displayCreateNumericQuestionDialog;
    displayEditNumericQuestionDialog = viewUtils.displayEditNumericQuestionDialog;
    updateMultipleChoiceQuestionDialogOptionsDisplay = viewUtils.updateMultipleChoiceQuestionDialogOptionsDisplay;
    displayCreateMultipleChoiceQuestionDialog = viewUtils.displayCreateMultipleChoiceQuestionDialog;
    displayEditMultipleChoiceQuestionDialog = viewUtils.displayEditMultipleChoiceQuestionDialog;
    displayCreateMultipleChoiceOptionDialog = viewUtils.displayCreateMultipleChoiceOptionDialog;
    updateQuestionDisplay = viewUtils.updateQuestionDisplay;
    displayCreateRulesetDialog = viewUtils.displayCreateRulesetDialog;
    displayCreateFlatRateRuleDialog = viewUtils.displayCreateFlatRateRuleDialog;
    displayEditFlatRateRuleDialog = viewUtils.displayEditFlatRateRuleDialog;
    displayCreateTieredRateRuleDialog = viewUtils.displayCreateTieredRateRuleDialog;
    displayEditTieredRateRuleDialog = viewUtils.displayEditTieredRateRuleDialog;
    displayCreateSecondaryTieredRateRuleDialog = viewUtils.displayCreateSecondaryTieredRateRuleDialog;
    displayEditSecondaryTieredRateRuleDialog = viewUtils.displayEditSecondaryTieredRateRuleDialog;
    displayCreateRuleTierDialog = viewUtils.displayCreateRuleTierDialog;
    displayEditRuleTierDialog = viewUtils.displayEditRuleTierDialog;
    displayCreateSecondaryRuleTierDialog = viewUtils.displayCreateSecondaryRuleTierDialog;
    displayEditSecondaryRuleTierDialog = viewUtils.displayEditSecondaryRuleTierDialog;
    updateRulesetsDisplay = viewUtils.updateRulesetsDisplay;
    validateBooleanQuestionDialog = viewUtils.validateBooleanQuestionDialog;
    validateNumericQuestionDialog = viewUtils.validateNumericQuestionDialog;
    validateMultipleChoiceQuestionDialog = viewUtils.validateMultipleChoiceQuestionDialog;
    validateMultipleChoiceOptionDialog = viewUtils.validateMultipleChoiceOptionDialog;
    validateRulesetDialog = viewUtils.validateRulesetDialog;
    validateRuleData = viewUtils.validateRuleData;
    validateFlatRateRuleDialog = viewUtils.validateFlatRateRuleDialog;
    validateTieredRateRuleDialog = viewUtils.validateTieredRateRuleDialog;
    validateSecondaryTieredRateRuleDialog = viewUtils.validateSecondaryTieredRateRuleDialog;
    validateRuleTierDialog = viewUtils.validateRuleTierDialog;
    validateSecondaryRuleTierDialog = viewUtils.validateSecondaryRuleTierDialog;
    displayValidationErrors = viewUtils.displayValidationErrors;
}

function doNothing() { }

/*
 * Dialog Actions
 */
// Appropriately manage app state when a dialog is cancelled
function cancelDialog(dialogId, shouldClearDialogState, shouldClearParentState) {
    hideDialog(dialogId);
    if (shouldClearDialogState) {
        clearDialogState();
    }

    if (shouldClearParentState) {
        clearParentState();
        app.parentRuleset = null;
    }
}

// Appropriately handle app state when a child dialog is cancelled
// A child dialog is one which is accessed exclusively via a parent dialog
// This includes option and rule tier dialogs
function cancelChildDialog(dialogId) {
    hideDialog(dialogId);
    moveParentStateToAppState();
}

// Appropriately handle app state when a confirmation dialog is cancelled
function cancelConfirmationDialog() {
    hideDialog(confirmationDialog.dialog.id);
    switch (app.dialogState.entityType) {
        case dialogStates.entityTypes.question:
                clearDialogState();
                clearParentState();
            break;
        case dialogStates.entityTypes.multipleChoiceOption:
                moveParentStateToAppState();
            break;
        case dialogStates.entityTypes.ruleset:
                clearDialogState();
                clearParentState();
            break;
        case dialogStates.entityTypes.rule:
                clearDialogState();
                clearParentState();
            break;
        case dialogStates.entityTypes.ruleTier:
                moveParentStateToAppState();
            break;
        case dialogStates.entityTypes.secondaryRuleTier:
                moveParentStateToAppState();
            break;
    }
}

/*
 * Forms Views
 */
// Update the app state and refresh the questions display when
// question data is successfully loaded
function displayQuestions(data) {
    app.jurisdictionForm = data;
    if (isAllJurisdictionsForm(app.jurisdictionForm)) {
        setCommonQuestions(app.jurisdictionForm);
    }
    refreshAppState();

    updateQuestionDisplay(app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].questions);
}

// Display an error when an attempt to load question data fails
function displayQuestionsLoadError() {
    error("An error occurred while loading questions for selected jurisdiction.");
}

/*
 * Jurisdiction Views
 */
// Event handler to be called when the selection in the jurisdiction select changes
function jurisdictionSelected() {
    jurisdictionId = getSelectedJurisdictionId();
    getFormForJurisdiction(jurisdictionId, displayQuestions, displayQuestionsLoadError);
    getRulesetsForJurisdiction(jurisdictionId, displayRulesets, displayRulesetsLoadError);
}

// Callback to initialise the jurisdiction select box
// when jurisdiction data is successfully loaded
function loadJurisdictionSelect(data) {
    app.jurisdictions = data.jurisdictions;

    initJurisdictionsSelect(app.jurisdictions, jurisdictionSelected);
    jurisdictionSelected();
}

// Display an error in the event that jurisdiction data fails to load
function displayJurisdictionLoadError() {
    error("An error occurred while loading jurisdictions.");
}

/*
 * Tax Category Views
 */
// Update the app state with tax category data when
// tax category data is loaded from the API
function loadTaxCategorySelect(data) {
    app.taxCategories = data;
}

// Display an error when tax category data fails to load correctly
function displayTaxCategoryLoadError() {
    error("An error occurred while loading tax categories.");
}

/*
 * Question Views
 */
// Trigger the call to reload question data from the forms API
function refreshQuestionsDisplay(refresher=getFormForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayQuestions, displayQuestionsLoadError);
}


// When a question type is selected via the question type dialog,
// display the correct question dialog to add or edit questions
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

// Display the appropriate question dialog to edit questions
// depending on the type of question to be edited
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

// When the call to save a question via the forms API successes, display a message
// and refresh the questions display
function saveQuestionSucceeded(data, textStatus, request, refresher=refreshQuestionsDisplay) {
    success("The question was successfully saved.");
    clearDialogState();
    refresher();
}

// Display an appropriate error message when saving a question fails
function saveQuestionFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to save question: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to save question.");
    }
}

// Save a question using the specified creators and updaters
// The appropriate creator or updater is used depending on the dialog mode (edit or create)
// and depending on the question type
function saveQuestion(booleanQuestionCreator=createBooleanQuestion, numericQuestionCreator=createNumericQuestion,
    multipleChoiceQuestionCreator=createMultipleChoiceQuestion, booleanQuestionUpdater=updateBooleanQuestion, numericQuestionUpdater=updateNumericQuestion,
    multipleChoiceQuestionUpdater=updateMultipleChoiceQuestion) {
    formId = getFormId();
    let errors = [];

    if (app.dialogState.mode == dialogStates.modes.create) {
        switch (app.dialogState.entityType) {
            // Create boolean question
            case dialogStates.entityTypes.booleanQuestion:
                    errors = validateBooleanQuestionDialog();
                    if (errors.length == 0) {
                        hideDialog(booleanQuestionDialog.dialog.id);
                        booleanQuestionCreator(
                            formId,
                            document.getElementById(booleanQuestionDialog.questionText.input.id).value,
                            getNextQuestionOrdinal(),
                            document.getElementById(booleanQuestionDialog.explainer.input.id).value,
                            document.getElementById(booleanQuestionDialog.variableName.input.id).value,
                            document.getElementById(booleanQuestionDialog.isMandatory.input.id).checked,
                            saveQuestionSucceeded,
                            saveQuestionFailed
                        );
                    } else {
                        displayValidationErrors(booleanQuestionDialog.errors.id, errors);
                    }
                break;
            // Create numeric question
            case dialogStates.entityTypes.numericQuestion:
                    errors = validateNumericQuestionDialog();
                    if (errors.length == 0) {
                        hideDialog(numericQuestionDialog.dialog.id);
                        numericQuestionCreator(
                            formId,
                            document.getElementById(numericQuestionDialog.questionText.input.id).value,
                            getNextQuestionOrdinal(),
                            document.getElementById(numericQuestionDialog.explainer.input.id).value,
                            document.getElementById(numericQuestionDialog.variableName.input.id).value,
                            document.getElementById(numericQuestionDialog.isMandatory.input.id).checked,
                            document.getElementById(numericQuestionDialog.isInteger.input.id).checked,
                            document.getElementById(numericQuestionDialog.minimumValue.input.id).value,
                            document.getElementById(numericQuestionDialog.maximumValue.input.id).value,
                            saveQuestionSucceeded,
                            saveQuestionFailed
                        );
                    } else {
                        displayValidationErrors(numericQuestionDialog.errors.id, errors);
                    }
                break;
            // Create multiple choice questions
            case dialogStates.entityTypes.multipleChoiceQuestion:
                    errors = validateMultipleChoiceQuestionDialog();
                    if (errors.length == 0) {
                        hideDialog(multipleChoiceQuestionDialog.dialog.id);
                        multipleChoiceQuestionCreator(
                            formId,
                            document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value,
                            getNextQuestionOrdinal(),
                            document.getElementById(multipleChoiceQuestionDialog.explainer.input.id).value,
                            document.getElementById(multipleChoiceQuestionDialog.variableName.input.id).value,
                            document.getElementById(multipleChoiceQuestionDialog.isMandatory.input.id).checked,
                            saveQuestionSucceeded,
                            saveQuestionFailed
                        );
                    } else {
                        displayValidationErrors(multipleChoiceQuestionDialog.errors.id, errors);
                    }
                break;
        }
        
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        question = app.dialogState.entity;

        switch(app.dialogState.entityType) {
            // Edit boolean question
            case dialogStates.entityTypes.booleanQuestion:
                    errors = validateBooleanQuestionDialog(question.id);
                    if (errors.length == 0) {
                        hideDialog(booleanQuestionDialog.dialog.id);
                        booleanQuestionUpdater(
                            formId,
                            question.id,
                            document.getElementById(booleanQuestionDialog.questionText.input.id).value,
                            question.ordinal,
                            document.getElementById(booleanQuestionDialog.explainer.input.id).value,
                            document.getElementById(booleanQuestionDialog.isMandatory.input.id).checked,
                            saveQuestionSucceeded,
                            saveQuestionFailed
                        );
                    } else {
                        displayValidationErrors(booleanQuestionDialog.errors.id, errors);
                    }
                break;
            // Edit numeric question
            case dialogStates.entityTypes.numericQuestion:
                    errors = validateNumericQuestionDialog(question.id);
                    if (errors.length == 0) {
                        hideDialog(numericQuestionDialog.dialog.id);
                        numericQuestionUpdater(
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
                    } else {
                        displayValidationErrors(numericQuestionDialog.errors.id, errors);
                    }
                break;
            // Edit multiple choice question
            case dialogStates.entityTypes.multipleChoiceQuestion:
                    errors = validateMultipleChoiceQuestionDialog(question.id);
                    if (errors.length == 0) {
                        hideDialog(multipleChoiceQuestionDialog.dialog.id);
                        multipleChoiceQuestionUpdater(
                            formId,
                            question.id,
                            document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value,
                            question.ordinal,
                            document.getElementById(multipleChoiceQuestionDialog.explainer.input.id).value,
                            document.getElementById(multipleChoiceQuestionDialog.isMandatory.input.id).checked,
                            saveQuestionSucceeded,
                            saveQuestionFailed
                        );
                    } else {
                        displayValidationErrors(multipleChoiceQuestionDialog.errors.id, errors);
                    }
                break;
        }
    } else {
        error("Invalid dialog mode " + app.dialogState.mode + " found when saving question.");
    }
}

// Callback to handle the successful deletion of a question
// When a question has been successfully deleted, then display a success message
// and resequence question ordinals
function deleteQuestionSucceeded(request, status, message, ordinalUpdater=updateQuestion, displayRefresher=refreshQuestionsDisplay) {
    success("The selected question was successfully deleted.");
    questions = resequenceQuestionOrdinals(app.dialogState.entity);
    let requestQueue = [];
    questions.forEach(question => {
        if (question.id != app.dialogState.entity.id) {
            requestQueue.push(question);
            //ordinalUpdater(question, doNothing, saveQuestionFailed);
        }
    });

    processBatch(
        requestQueue,
        function(question) { ordinalUpdater(question, doNothing, saveQuestionFailed); },
        function() {
            clearDialogState();
            displayRefresher();
        }
    );
}

// Callback to handle the case where a question fails to be deleted for any reason
function deleteQuestionFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to delete question: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to delete question.");
    }
}

// Action to confirm the deletion of a question
// Hide the confirmation dialog and trigger the API call
function confirmDeleteQuestion(event, remover=removeQuestion) {
    hideDialog(confirmationDialog.dialog.id);
    formId = getFormId();
    question = app.dialogState.entity;
    remover(formId, question.id, deleteQuestionSucceeded, deleteQuestionFailed);
}

// Event handler to handle the user clicking on the delete question button
// Check to make sure the question doesn't have any dependent rules
// A rule is dependent if it lists the question's variable as its variable name
// If so, display an error. Otherwise, set the app state and display the confirmation dialog
function deleteQuestion(question) {
    if (!questionHasDependentRules(question.id)) {
        setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.question, question);
        confirm("Please confirm you wish for the following question to be deleted: " + question.text + ".", confirmDeleteQuestion);
    } else {
        error("The following question cannot be deleted as rules exist which depend on this question: '" + question.text + "'. Please delete dependent rules first.");
    }
}

// Swap the ordinals of two questions
// The first question is specified while the second question is determined
// by the given findNewPosition function which should return the question
// to swap with
// Save the ordinal changes via the API
function swapQuestionOrdinals(question, findNewPosition, updater, refresher) {
    // Find the question that needs to be swapped
    let questionToSwap = findNewPosition(question);

    if (questionToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = question.ordinal;
        question.ordinal = questionToSwap.ordinal;
        questionToSwap.ordinal = originalOrdinal;

        // Save the questions
        let update1 = updater(question, doNothing, saveQuestionFailed);
        let update2 = updater(questionToSwap, doNothing, saveQuestionFailed);

        // Refresh the question display when both updates have completed
        // Taken from https://www.codeproject.com/Articles/1181613/Waiting-For-Multiple-Ajax-Requests-jQuery
        $.when(update1, update2).then(function () {
            refresher();
        });
    }
}

// Swap the selected question's ordinal with the question whose ordinal immediately precedes
// that of the selected question
function moveQuestionUp(question, updater=updateQuestion, refresher=refreshQuestionsDisplay) {
    swapQuestionOrdinals(question, findPreviousQuestion, updater, refresher);
}

// Swap the selected question's ordinal with the question whose ordinal immediately follows
// that of the selected question
function moveQuestionDown(question, updater=updateQuestion, refresher=refreshQuestionsDisplay) {
    swapQuestionOrdinals(question, findNextQuestion, updater, refresher);
}

/*
 * Multiple Choice Option Views
 */
// Callback to handle the successful retrieval of multiple choice options
// data for a given question
// When multiple choice options data is successfully loaded, update the
// app state and display the data in the question dialog
// App state is updating by saving the latest data to the app state
// and, since the multiple choice options are a child state of questions,
// move the question state back into the currently-active dialog state
function displayMultipleChoiceOptions(data) {
    app.jurisdictionForm = data;
    refreshAppState();

    if (app.parentState.entity != null) {
        if (app.parentState.entityType == dialogStates.entityTypes.multipleChoiceQuestion) {
            moveParentStateToAppState();
        }
    }

    question = findQuestionById(app.dialogState.entity.id);
    options = question.options;
    updateMultipleChoiceQuestionDialogOptionsDisplay(options);    
}

// Display an error if multiple choice options data fails to load
function displayMultipleChoiceOptionsError(request, status, message) {
    error("An error occurred while refreshing multiple choice options for question " + app.dialogState.entity.name);
}

// Trigger the API call to get the latest multiple choice options data
function refreshMultipleChoiceOptionsDisplay(refresher=getFormForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayMultipleChoiceOptions, displayMultipleChoiceOptionsError);
}

// Callback to handle successful saves of multiple choice option data
// Display a success message, update the app state and then refresh the display
function saveMultipleChoiceOptionSucceeded(data, textStatus, request, refresher=refreshMultipleChoiceOptionsDisplay) {
    success("The option was successfully saved.");
    moveParentStateToAppState();
    refresher();
}

// Callback to handle failed saves of multiple choice options data
// Display an error message
function saveMultipleChoiceOptionFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to save multiple choice option: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to save multiple choice option.");
    }
}

// Save a multiple choice option
// Hide the create/edit multiple choice options dialog,
// get the required data from the app state and dialog
// validate the data and then trigger the API call
function saveMultipleChoiceOption(creator=postMultipleChoiceOption) {
    let errors = validateMultipleChoiceOptionDialog();
    if (errors.length == 0) {
        hideDialog(multipleChoiceOptionDialog.dialog.id);

        let formId = getFormId();
        let questionId = app.parentState.entity.id;
        let name = document.getElementById(multipleChoiceOptionDialog.name.input.id).value;
        let explainer = document.getElementById(multipleChoiceOptionDialog.explainer.input.id).value;

        if (app.dialogState.mode == dialogStates.modes.create) {
            creator(formId, questionId, name, explainer, saveMultipleChoiceOptionSucceeded, saveMultipleChoiceOptionFailed);
        }
    } else {
        displayValidationErrors(multipleChoiceOptionDialog.errors.id, errors);
    }
}

// Event handler for the create multiple choice option button clicked event
// Set app state and display the create dialog
function createMultipleChoiceOption() {
    moveAppStateToParentState();
    setDialogState(dialogStates.modes.create, dialogStates.entityTypes.multipleChoiceOption, null);
    displayCreateMultipleChoiceOptionDialog();
}

// Handle delete multiple choice option success events
function deleteMultipleChoiceOptionSucceeded(request, status, message, displayRefresher=refreshMultipleChoiceOptionsDisplay) {
    showDialog(multipleChoiceQuestionDialog.dialog.id);
    displayRefresher();
}

// Handle delete multiple choice option failure events
// Show an appropriate error message
function deleteMultipleChoiceOptionFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to delete option: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to delete option.");
    }
    
    moveParentStateToAppState();
    clearParentState();
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

// Action to confirm delete multiple choice option
// Hide the confirmation dialog and then trigger the API call to remove
// the selected option
function confirmDeleteMultipleChoiceOption(event, remover=removeMultipleChoiceOption) {
    hideDialog(confirmationDialog.dialog.id);
    formId = getFormId();
    question = app.parentState.entity;
    option = app.dialogState.entity;
    remover(formId, question.id, option.id, deleteMultipleChoiceOptionSucceeded, deleteMultipleChoiceOptionFailed);
}

// Action to handle the user choosing to delete a multiple choice option
// Set the app state and display the confirmation dialog
function deleteMultipleChoiceOption(option) {
    moveAppStateToParentState();
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.multipleChoiceOption, option);
    confirm("Please confirm you wish for the following option to be deleted: " + option.text + ".", confirmDeleteMultipleChoiceOption);
}

/*
 * Ruleset Views
 */
// Handle the successful load of rulesets and rule data
// Update both the app state and then refresh the rulesets display
function displayRulesets(data) {
    app.jurisdictionRules = data;
    refreshAppState();

    updateRulesetsDisplay(app.jurisdictionRules);
}

// Handle failures to load rulesets and rule data
// Display an appropriate error message
function displayRulesetsLoadError() {
    error("An error occurred while loading rulesets for selected jurisdiction.");
}

// Helper function to trigger the refresh of rulesets and rule data
// Get the selected jurisdiction and then refresh the data
function refreshRulesetsDisplay(refresher=getRulesetsForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayRulesets, displayRulesetsLoadError);
}

// Handler for successful saves of ruleset data
// Display a success message, clear the dialog state and refresh the display
function saveRulesetSucceeded(data, textStatus, request, refresher=refreshRulesetsDisplay) {
    success("The ruleset was successfully saved.");
    clearDialogState();
    refresher();
}

// Handler for failures to save ruleset data
// Display an appropriate error message
function saveRulesetFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to save ruleset: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to save ruleset.");
    }
}

// Action to save ruleset
// Validate the data and if all is clear, hide the dialog and trigger the call to the API
// Otherwise display validation errors
function saveRuleset(creator=postRuleset) {
    let errors = validateRulesetDialog();
    if (errors.length == 0) {
        hideDialog(rulesetDialog.dialog.id);

        jurisdictionId = getSelectedJurisdictionId();
        taxCategoryId = document.getElementById(rulesetDialog.taxCategory.input.id).value;
        ordinal = getNextRulesetOrdinal();

        if (app.dialogState.mode == dialogStates.modes.create) {
            creator(jurisdictionId, taxCategoryId, ordinal, saveRulesetSucceeded, saveRulesetFailed);
        }
    } else {
        displayValidationErrors(rulesetDialog.errors.id, errors);
    }
}

// Action to create a new ruleset
// Set the app state and display the create ruleset dialog
function createRuleset() {
    setDialogState(dialogStates.modes.create, dialogStates.entityTypes.ruleset, null);
    displayCreateRulesetDialog();
}

// Event handler for successful deletion of rulesets
// Display a success message and then resequence ordinals, saving refreshed ordinals via
// the API
function deleteRulesetSucceeded(data, textStatus, request, ordinalUpdater=patchRuleset, displayRefresher=refreshRulesetsDisplay) {
    success("The selected ruleset was successfully deleted.");
    rulesets = resequenceRulesetOrdinals(app.dialogState.entity);
    let requestQueue = [];
    rulesets.forEach(ruleset => {
        if (ruleset.id != app.dialogState.entity.id) {
            requestQueue.push(ruleset);
        }
    });

    processBatch(
        requestQueue,
        function(ruleset) { ordinalUpdater(ruleset.id, ruleset.ordinal, doNothing, saveRulesetFailed); },
        function() { 
            clearDialogState();
            displayRefresher();
        });
}

// Event handler for failed deletion of rulesets
// Display an appropriate error message
function deleteRulesetFailed() {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to delete ruleset: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to delete ruleset.");
    }
}

// Action to confirm deletion of a ruleset
// Hide the confirmation dialog and trigger deletion via the API
function confirmDeleteRuleset(event, remover=removeRuleset) {
    hideDialog(confirmationDialog.dialog.id);
    remover(app.dialogState.entity.id, deleteRulesetSucceeded, deleteRulesetFailed);
}

// Action to trigger deletion of a ruleset
// Set the app state and display the confirmation dialog
function deleteRuleset(ruleset) {
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleset, ruleset);
    confirm("Please confirm you wish for the following ruleset to be deleted: " + ruleset.name + ".", confirmDeleteRuleset);
}

// Helper function to swap the ordinals of two rulesets
// One ruleset is specified and the other is determined by the specified function
// Once ordinals have been swapped, update the ordinals via the API and refresh the display
function swapRulesetOrdinals(ruleset, findNewPosition, updater, refresher) {
    // Find the ruleset that needs to be swapped
    let rulesetToSwap = findNewPosition(ruleset);

    if (rulesetToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = ruleset.ordinal;
        ruleset.ordinal = rulesetToSwap.ordinal;
        rulesetToSwap.ordinal = originalOrdinal;

        // Save the rulesets
        let update1 = updater(ruleset.id, ruleset.ordinal, doNothing, saveRulesetFailed);
        let update2 = updater(rulesetToSwap.id, rulesetToSwap.ordinal, doNothing, saveRulesetFailed);

        // Refresh the ruleset display when both updates have completed
        // Taken from https://www.codeproject.com/Articles/1181613/Waiting-For-Multiple-Ajax-Requests-jQuery
        $.when(update1, update2).then(function () {
            refresher();
        });
    }
}

// Action to move a ruleset up by swapping its ordinal with that of the immediately preceding ruleset
function moveRulesetUp(ruleset, updater=patchRuleset, refresher=refreshRulesetsDisplay) {
    swapRulesetOrdinals(ruleset, findPreviousRuleset, updater, refresher);
}

// Action to move a ruleset up by swapping its ordinal with that of the ruleset that immediately follows
function moveRulesetDown(ruleset, updater=patchRuleset, refresher=refreshRulesetsDisplay) {
    swapRulesetOrdinals(ruleset, findNextRuleset, updater, refresher);
}

/*
 * Rule Views
 */
// Action to add a new rule
// Set the parent ruleset and the show the dialog
function addRule(ruleset) {
    setParentRuleset(ruleset);
    showDialog(ruleTypeDialog.dialog.id);
}

// Action to edit a rule
// Set the parent ruleset and app state then display the appropriate
// dialog for the type of rule to be edited
function editRule(ruleset, rule) {
    setParentRuleset(ruleset);
    switch (rule.type) {
        case "flat_rate":
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.flatRateRule, rule);
                displayEditFlatRateRuleDialog(rule);
            break;
        case "tiered_rate":
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);
                displayEditTieredRateRuleDialog(rule);
            break;
        case "secondary_tiered_rate":
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryTieredRateRule, rule);
                primary_rules = getTieredRateRulesForJurisdiction();
                displayEditSecondaryTieredRateRuleDialog(rule, primary_rules);
            break;
    }
}

// Handle selection of a rule type via the rule type dialog
// Used when creating a new rule
// Hide the dialog, set the app state, and then display the appropriate dialog
// for the selected type of rule
function ruleTypeSelected() {
    // Hide rule type dialog
    hideDialog(ruleTypeDialog.dialog.id);

    // Get the rule type
    ruleType = document.getElementById(ruleTypeDialog.ruleType.input.id).value;

    // Trigger the appropriate create dialog
    switch(ruleType) {
        case "flat_rate":
                setDialogState(dialogStates.modes.create, dialogStates.entityTypes.flatRateRule, null);
                displayCreateFlatRateRuleDialog();
            break;
        case "tiered_rate":
                setDialogState(dialogStates.modes.create, dialogStates.entityTypes.tieredRateRule, null);
                displayCreateTieredRateRuleDialog();
            break;
        case "secondary_tiered_rate":
                primaryRules = getTieredRateRulesForJurisdiction();
                setDialogState(dialogStates.modes.create, dialogStates.entityTypes.secondaryTieredRateRule, null);
                displayCreateSecondaryTieredRateRuleDialog(primaryRules);
            break;
    }
}

// Callback function to handle successful saves of rule data
// Display a success message, clear the dialog state and then refresh the display
function saveRuleSucceeded(data, textStatus, request, refresher=refreshRulesetsDisplay) {
    success("The rule was successfully saved.");
    clearDialogState();
    refresher();
}

// Callback to handle failed saves of rule data
// Display an appropriate error message
function saveRuleFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to save rule: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to save rule.");
    }
}

// Action to save a rule
// Depending on the type of rule to be saved, and on the dialog mode (create or edit):
// validate the dialog data, and if there are errors display them.
// Otherwise, hide the dialog and trigger the save via the appropriate API
function saveRule(flatRateRuleCreator=createFlatRateRule, tieredRateRuleCreator=createTieredRateRule,
    secondaryTieredRateRuleCreator=createSecondaryTieredRateRule, flatRateRuleUpdater=updateFlatRateRule, tieredRateRuleUpdater=updateTieredRateRule,
    secondaryTieredRateRuleUpdater=updateSecondaryTieredRateRule) {
    rulesetId = app.parentRuleset.id;

    let errors = [];

    if (app.dialogState.mode == dialogStates.modes.create) {
        switch (app.dialogState.entityType) {
            // Create flat rate rule
            case dialogStates.entityTypes.flatRateRule:
                    errors = validateFlatRateRuleDialog();
                    if (errors.length == 0) {
                        hideDialog(flatRateRuleDialog.dialog.id);
                        flatRateRuleCreator(
                            rulesetId,
                            document.getElementById(flatRateRuleDialog.name.input.id).value,
                            document.getElementById(flatRateRuleDialog.explainer.input.id).value,
                            document.getElementById(flatRateRuleDialog.variableName.input.id).value,
                            getNextRuleOrdinal(),
                            document.getElementById(flatRateRuleDialog.taxRate.input.id).value,
                            saveRuleSucceeded,
                            saveRuleFailed
                        );
                    } else {
                        displayValidationErrors(flatRateRuleDialog.errors.id, errors);
                    }
                break;
            // Create tiered rate rule
            case dialogStates.entityTypes.tieredRateRule:
                    errors = validateTieredRateRuleDialog();
                    if (errors.length == 0) {
                        hideDialog(tieredRateRuleDialog.dialog.id);
                        tieredRateRuleCreator(
                            rulesetId,
                            document.getElementById(tieredRateRuleDialog.name.input.id).value,
                            document.getElementById(tieredRateRuleDialog.explainer.input.id).value,
                            document.getElementById(tieredRateRuleDialog.variableName.input.id).value,
                            getNextRuleOrdinal(),
                            saveRuleSucceeded,
                            saveRuleFailed
                        );
                    } else {
                        displayValidationErrors(tieredRateRuleDialog.errors.id, errors);
                    }
                break;
            // Create secondary tiered rate rule
            case dialogStates.entityTypes.secondaryTieredRateRule:
                    errors = validateSecondaryTieredRateRuleDialog();
                    if (errors.length == 0) {
                        hideDialog(secondaryTieredRateRuleDialog.dialog.id);
                        secondaryTieredRateRuleCreator(
                            rulesetId,
                            document.getElementById(secondaryTieredRateRuleDialog.name.input.id).value,
                            document.getElementById(secondaryTieredRateRuleDialog.explainer.input.id).value,
                            document.getElementById(secondaryTieredRateRuleDialog.variableName.input.id).value,
                            getNextRuleOrdinal(),
                            document.getElementById(secondaryTieredRateRuleDialog.primaryRule.input.id).value,
                            saveRuleSucceeded,
                            saveRuleFailed
                        );
                    } else {
                        displayValidationErrors(secondaryTieredRateRuleDialog.errors.id, errors);
                    }
                break;
        }
        
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        rule = app.dialogState.entity;
        switch(app.dialogState.entityType) {
            // Edit flat rate rule
            case dialogStates.entityTypes.flatRateRule:
                    errors = validateFlatRateRuleDialog();
                    if (errors.length == 0) {
                        hideDialog(flatRateRuleDialog.dialog.id);
                        flatRateRuleUpdater(
                            rulesetId,
                            rule.id,
                            document.getElementById(flatRateRuleDialog.name.input.id).value,
                            document.getElementById(flatRateRuleDialog.explainer.input.id).value,
                            document.getElementById(flatRateRuleDialog.variableName.input.id).value,
                            rule.ordinal,
                            document.getElementById(flatRateRuleDialog.taxRate.input.id).value,
                            saveRuleSucceeded,
                            saveRuleFailed
                        );
                    } else {
                        displayValidationErrors(flatRateRuleDialog.errors.id, errors);
                    }
                break;
            // Edit tiered rate rule
            case dialogStates.entityTypes.tieredRateRule:
                    errors = validateTieredRateRuleDialog();
                    if (errors.length == 0) {
                        hideDialog(tieredRateRuleDialog.dialog.id);
                        tieredRateRuleUpdater(
                            rulesetId,
                            rule.id,
                            document.getElementById(tieredRateRuleDialog.name.input.id).value,
                            document.getElementById(tieredRateRuleDialog.explainer.input.id).value,
                            document.getElementById(tieredRateRuleDialog.variableName.input.id).value,
                            rule.ordinal,
                            saveRuleSucceeded,
                            saveRuleFailed
                        );
                    } else {
                        displayValidationErrors(tieredRateRuleDialog.errors.id, errors);
                    }
                break;
            // Edit secondary tiered rate rule
            case dialogStates.entityTypes.secondaryTieredRateRule:
                    errors = validateSecondaryTieredRateRuleDialog();
                    if (errors.length == 0) {
                        hideDialog(secondaryTieredRateRuleDialog.dialog.id);
                        secondaryTieredRateRuleUpdater(
                            rulesetId,
                            rule.id,
                            document.getElementById(secondaryTieredRateRuleDialog.name.input.id).value,
                            document.getElementById(secondaryTieredRateRuleDialog.explainer.input.id).value,
                            document.getElementById(secondaryTieredRateRuleDialog.variableName.input.id).value,
                            rule.ordinal,
                            document.getElementById(secondaryTieredRateRuleDialog.primaryRule.input.id).value,
                            saveRuleSucceeded,
                            saveRuleFailed
                        );
                    } else {
                        displayValidationErrors(secondaryTieredRateRuleDialog.errors.id, errors);
                    }
                break;
        }
    } else {
        error("Invalid dialog mode " + app.dialogState.mode + " found when saving question.");
    }
}

// Event handler for successful deletion of a rule
// Display a success message, resequence rule ordinals, and then save the resequenced ordinals
// via the API
function deleteRuleSucceeded(data, textStatus, request, flatRateRuleUpdater=updateFlatRateRule, tieredRateRuleUpdater=updateTieredRateRule,
    secondaryTieredRateRuleUpdater=updateSecondaryTieredRateRule, displayRefresher=refreshRulesetsDisplay) {

    success("The selected rule was successfully deleted.");
    rules = resequenceRuleOrdinals(app.dialogState.entity);
    let requestQueue = [];
    rules.forEach(rule => {
        if (rule.id != app.dialogState.entity.id) {
            requestQueue.push(rule);
        }
    });

    processBatch(
        requestQueue,
        function(rule) {
            updateRule(
                findParentRuleset(rule.id).id,
                rule,
                flatRateRuleUpdater,
                tieredRateRuleUpdater,
                secondaryTieredRateRuleUpdater,
                doNothing,
                saveRuleFailed
            );
        },
        function() {
            clearDialogState();
            displayRefresher();
        }
    );
}

// Event handler for rule deletion failures
// Display an appropriate message
function deleteRuleFailed() {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to delete rule: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to delete rule.");
    }
}

// Action to confirm deletion of a rule
// Hide the dialog and then remove the rule via the API
function confirmDeleteRule(event, remover=removeRule) {
    hideDialog(confirmationDialog.dialog.id);
    remover(app.parentRuleset.id, app.dialogState.entity.id, deleteRuleSucceeded, deleteRuleFailed);
}

// Action to delete a rule
// If the rule is a tiered rate rule, check whether or not the rule has dependent secondary rules
// If so, display an error
// Otherwise set the app state and display the confirmation dialog
function deleteRule(ruleset, rule) {
    let proceed = true;
    if (rule.type == "tiered_rate") {
        if (primaryRuleHasDependentSecondaryRules(rule.id)) {
            error("The following rule cannot be deleted as secondary rules exist which depend on it: '" + rule.name + "'. Please delete dependent secondary rules first.");
            proceed = false;
        }
    }
    if (proceed) {
        setParentRuleset(ruleset);
        setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.rule, rule);
        confirm("Please confirm you wish for the following rule to be deleted: " + rule.name + ".", confirmDeleteRule);
    }
}

// Helper function to save the rule ordinals for a given rule
// Allows a rule to be updated depending on its type without updating
// the app state
function updateRuleOrdinal(ruleset, rule) {
    switch(rule.type) {
        case "flat_rate":
                updateFlatRateRule(
                    ruleset.id,
                    rule.id,
                    rule.name,
                    rule.explainer,
                    rule.variable_name,
                    rule.ordinal,
                    rule.tax_rate,
                    doNothing,
                    saveRuleFailed
                );
            break;
        case "tiered_rate":
                updateTieredRateRule(
                    ruleset.id,
                    rule.id,
                    rule.name,
                    rule.explainer,
                    rule.variable_name,
                    rule.ordinal,
                    doNothing,
                    saveRuleFailed
                );
            break;
        case "secondary_tiered_rate":
                updateSecondaryTieredRateRule(
                    ruleset.id,
                    rule.id,
                    rule.name,
                    rule.explainer,
                    rule.variable_name,
                    rule.ordinal,
                    rule.primary_rule.id,
                    doNothing,
                    saveRuleFailed
                );
            break;
    }
}

// Swap the ordinals for two rules within a ruleset
function swapRuleOrdinals(ruleset, rule, findNewPosition, updater, refresher) {
    // Find the rule that needs to be swapped
    let ruleToSwap = findNewPosition(ruleset, rule);

    if (ruleToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = rule.ordinal;
        rule.ordinal = ruleToSwap.ordinal;
        ruleToSwap.ordinal = originalOrdinal;

        // Save the ordinals
        let update1 = updater(ruleset, rule);
        let update2 = updater(ruleset, ruleToSwap);

        // Refresh the ruleset display when both updates have completed
        // Taken from https://www.codeproject.com/Articles/1181613/Waiting-For-Multiple-Ajax-Requests-jQuery
        $.when(update1, update2).then(function () {
            refresher();
        });
    }
}

// Swap a rule with the one immediately preceding it based on ordinals
function moveRuleUp(ruleset, rule, updater=updateRuleOrdinal, refresher=refreshRulesetsDisplay) {
    swapRuleOrdinals(ruleset, rule, findPreviousRule, updater, refresher);
}

// Swap a rule with the one immediately following it based on ordinals
function moveRuleDown(ruleset, rule, updater=updateRuleOrdinal, refresher=refreshRulesetsDisplay) {
    swapRuleOrdinals(ruleset, rule, findNextRule, updater, refresher);
}

/*
 * Rule Tier Views
 */
function displayRuleTiersLoadedSucceeded(data, textStatus, request) {
    app.jurisdictionRules = data;
    refreshAppState();

    if (app.parentState.entity != null) {
        moveParentStateToAppState();
    }

    rule = findRuleById(app.dialogState.entity.id);
    tiers = rule.tiers;
    switch(app.dialogState.entityType) {
        case dialogStates.entityTypes.tieredRateRule:
                updateRuleTierTable(true, tiers);
            break;
        case dialogStates.entityTypes.secondaryTieredRateRule:
                updateRuleTierTable(false, tiers);
            break;
    }
}

function displayRuleTiersLoadedError(request, status, message) {
    error("An error occurred while refreshing rule tiers for rule " + app.parentState.entity.name);
}

function refreshRuleTiersDisplay(refresher=getRulesetsForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayRuleTiersLoadedSucceeded, displayRuleTiersLoadedError);
}

function saveRuleTierSucceeded(data, textStatus, request, refresher=refreshRuleTiersDisplay) {
    success("The tier was successfully saved.");
    moveParentStateToAppState();
    refresher();
}

function saveRuleTierFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to save rule tier: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to save rule tier.");
    }
}

function saveRuleTier(ruleTierCreator=postRuleTier, secondaryRuleTierCreator=postSecondaryRuleTier, ruleTierUpdater=updateRuleTier,
    secondaryRuleTierUpdater=updateSecondaryRuleTier) {
    rule = app.parentState.entity;
    ruleset = findParentRuleset(rule.id);

    let errors = [];

    if (app.dialogState.mode == dialogStates.modes.create)
    {
        switch (app.dialogState.entityType) {
            case dialogStates.entityTypes.ruleTier:
                    errors = validateRuleTierDialog();
                    if (errors.length == 0) {
                        hideDialog(ruleTierDialog.dialog.id);
                        ruleTierCreator(
                            ruleset.id,
                            rule.id,
                            document.getElementById(ruleTierDialog.minimumValue.input.id).value,
                            document.getElementById(ruleTierDialog.maximumValue.input.id).value,
                            getNextRuleTierOrdinal(rule),
                            document.getElementById(ruleTierDialog.taxRate.input.id).value,
                            saveRuleTierSucceeded,
                            saveRuleTierFailed
                        );
                    } else {
                        displayValidationErrors(ruleTierDialog.errors.id, errors);
                    }
                break;
            case dialogStates.entityTypes.secondaryRuleTier:
                    errors = validateSecondaryRuleTierDialog();
                    if (errors.length == 0) {
                        hideDialog(secondaryRuleTierDialog.dialog.id);
                        secondaryRuleTierCreator(
                            ruleset.id,
                            rule.id,
                            document.getElementById(secondaryRuleTierDialog.primaryTier.input.id).value,
                            getNextRuleTierOrdinal(rule),
                            document.getElementById(secondaryRuleTierDialog.taxRate.input.id).value,
                            saveRuleTierSucceeded,
                            saveRuleTierFailed
                        );
                    } else {
                        displayValidationErrors(ruleTierDialog.errors.id, errors);
                    }
                break;
        }
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        tier = app.dialogState.entity;
        switch (app.dialogState.entityType) {
            case dialogStates.entityTypes.ruleTier:
                    errors = validateRuleTierDialog();
                    if (errors.length == 0) {
                        hideDialog(ruleTierDialog.dialog.id);
                        ruleTierUpdater(
                            ruleset.id,
                            rule.id,
                            tier.id,
                            document.getElementById(ruleTierDialog.minimumValue.input.id).value,
                            document.getElementById(ruleTierDialog.maximumValue.input.id).value,
                            tier.ordinal,
                            document.getElementById(ruleTierDialog.taxRate.input.id).value,
                            saveRuleTierSucceeded,
                            saveRuleTierFailed
                        );
                    } else {
                        displayValidationErrors(ruleTierDialog.errors.id, errors);
                    }
                break;
            case dialogStates.entityTypes.secondaryRuleTier:
                    errors = validateSecondaryRuleTierDialog();
                    if (errors.length == 0) {
                        hideDialog(secondaryRuleTierDialog.dialog.id);
                        secondaryRuleTierUpdater(
                            ruleset.id,
                            rule.id,
                            tier.id,
                            tier.primary_tier_id,
                            tier.ordinal,
                            document.getElementById(secondaryRuleTierDialog.taxRate.input.id).value,
                            saveRuleTierSucceeded,
                            saveRuleTierFailed
                        );
                    } else {
                        displayValidationErrors(secondaryRuleTierDialog.errors.id, errors);
                    }
                break;
        }
    }
}

function createRuleTier(createPrimary) {
    moveAppStateToParentState();
    if (createPrimary) {
        setDialogState(dialogStates.modes.create, dialogStates.entityTypes.ruleTier, null);
        displayCreateRuleTierDialog();
    } else {
        primaryTiers = app.parentState.entity.primary_rule.tiers;
        setDialogState(dialogStates.modes.create, dialogStates.entityTypes.secondaryRuleTier, null);
        displayCreateSecondaryRuleTierDialog(primaryTiers);
    }
}

function editRuleTier(editPrimary, tier) {
    moveAppStateToParentState();
    if (editPrimary) {
        setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.ruleTier, tier);
        displayEditRuleTierDialog(tier);
    } else {
        primaryTiers = app.parentState.entity.primary_rule.tiers;
        setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryRuleTier, tier);
        displayEditSecondaryRuleTierDialog(tier, primaryTiers);
    }
}

function saveRuleTierOrdinal(isPrimary, tier) {
    rule = app.dialogState.entity;
    ruleset = findParentRuleset(rule.id);
    if (isPrimary) {
        updateRuleTier(
            ruleset.id,
            rule.id,
            tier.id,
            tier.min_value,
            tier.max_value,
            tier.ordinal,
            tier.tier_rate,
            doNothing,
            saveRuleTierFailed
        );
    } else {
        updateSecondaryRuleTier(
            ruleset.id,
            rule.id,
            tier.id,
            tier.primary_tier_id,
            tier.ordinal,
            tier.tier_rate,
            doNothing,
            saveRuleTierFailed
        );
    }
}

function swapRuleTierOrdinals(swapPrimary, tier, findNewPosition, updater, refresher) {
    // Find the tier that needs to be swapped
    let tierToSwap = findNewPosition(app.dialogState.entity, tier);

    if (tierToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = tier.ordinal;
        tier.ordinal = tierToSwap.ordinal;
        tierToSwap.ordinal = originalOrdinal;

        // Save the questions
        let update1 = updater(swapPrimary, tier);
        let update2 = updater(swapPrimary, tierToSwap);

        // Refresh the ruleset display
        // Taken from https://www.codeproject.com/Articles/1181613/Waiting-For-Multiple-Ajax-Requests-jQuery
        $.when(update1, update2).then(function() {
            refresher();
        });
    }
}

function moveRuleTierUp(isPrimary, tier, updater=saveRuleTierOrdinal, refresher=refreshRuleTiersDisplay) {
    swapRuleTierOrdinals(isPrimary, tier, findPreviousRuleTier, updater, refresher);
}

function moveRuleTierDown(isPrimary, tier, updater=saveRuleTierOrdinal, refresher=refreshRuleTiersDisplay) {
    swapRuleTierOrdinals(isPrimary, tier, findNextRuleTier, updater, refresher);
}

function deleteRuleTierSucceeded(data, textStatus, request, primaryTierUpdater=updateRuleTier,
    secondaryTierUpdater=updateSecondaryRuleTier, displayRefresher=refreshRuleTiersDisplay) {
    success("The selected rule tier was successfully deleted.");
    rule = app.parentState.entity;
    ruleset = findParentRuleset(rule.id);

    tiers = resequenceRuleTierOrdinals(app.dialogState.entity);
    let requestQueue = [];
    tiers.forEach(tier => {
        if (tier.id != app.dialogState.entity.id) {
            requestQueue.push(tier);
        }
    });
    if (app.dialogState.entityType == dialogStates.entityTypes.ruleTier) {
        processBatch(
            requestQueue,
            function(tier) { 
                primaryTierUpdater(
                    ruleset.id,
                    rule.id,
                    tier.id,
                    tier.min_value,
                    tier.max_value,
                    tier.ordinal,
                    tier.tier_rate,
                    doNothing,
                    saveRuleTierFailed
                );
             },
             function() {
                moveParentStateToAppState();
                displayRefresher();
             }
        );
    } else if (app.dialogState.entityType == dialogStates.entityTypes.secondaryRuleTier) {
        processBatch(
            requestQueue,
            function(tier) { 
                secondaryTierUpdater(
                    ruleset.id,
                    rule.id,
                    tier.id,
                    tier.primary_tier_id,
                    tier.ordinal,
                    tier.tier_rate,
                    doNothing,
                    saveRuleTierFailed
                );
             },
             function() {
                moveParentStateToAppState();
                displayRefresher();
             }
        );
    }
}

function deleteRuleTierFailed(request, status, message) {
    try {
        errorMsg = request.responseJSON.error;
        error("An error occurred while attempting to delete rule tier: " + errorMsg);
    } catch(ex) {
        error("An error occurred while attempting to delete rule tier.");
    }
    moveParentStateToAppState();
}

function confirmDeleteRuleTier(event, primaryRemover=removeRuleTier, secondaryRemover=removeSecondaryRuleTier) {
    hideDialog(confirmationDialog.dialog.id);

    tier = app.dialogState.entity;
    rule = app.parentState.entity;
    ruleset = findParentRuleset(rule.id);

    switch(app.dialogState.entityType) {
        case dialogStates.entityTypes.ruleTier:
                primaryRemover(ruleset.id, rule.id, tier.id, deleteRuleTierSucceeded, deleteRuleTierFailed);
            break;
        case dialogStates.entityTypes.secondaryRuleTier:
                secondaryRemover(ruleset.id, rule.id, tier.id, deleteRuleTierSucceeded, deleteRuleTierFailed);
            break;
    }
}

function deleteRuleTier(isPrimary, tier) {
    moveAppStateToParentState();
    if (isPrimary) {
        if (!primaryRuleTierHasDependentSecondaryTiers(tier.id)) {
            setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleTier, tier);
            confirm("Please confirm you wish for the selected rule tier to be deleted.", confirmDeleteRuleTier);
        } else {
            error("The selected tier cannot be deleted as secondary tiers exist which depend on it. Please delete dependent secondary tiers first.");
        }
    } else {
        setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.secondaryRuleTier, tier);
        confirm("Please confirm you wish for the selected rule tier to be deleted.", confirmDeleteRuleTier);
    }
}

/*
 * Initialisation functions
 */
function init() {
    setApiHost(window.location.protocol, window.location.hostname);
    getJurisdictions(loadJurisdictionSelect, displayJurisdictionLoadError);
    getTaxCategories(loadTaxCategorySelect, displayTaxCategoryLoadError);
}

if (typeof module !== "undefined") {
    module.exports = {
        doNothing,
        displayQuestionsLoadError,
        displayJurisdictionLoadError,
        displayTaxCategoryLoadError,
        saveQuestionFailed,
        deleteQuestionFailed,
        displayMultipleChoiceOptionsError,
        saveMultipleChoiceOptionFailed,
        deleteMultipleChoiceOptionFailed,
        displayRulesetsLoadError,
        saveRulesetFailed,
        deleteRulesetFailed,
        saveRuleFailed,
        deleteRuleFailed,
        displayRuleTiersLoadedError,
        saveRuleTierFailed,
        deleteRuleTierFailed,
        confirmDeleteQuestion,
        confirmDeleteMultipleChoiceOption,
        displayQuestions,
        loadJurisdictionSelect,
        loadTaxCategorySelect,
        refreshQuestionsDisplay,
        questionTypeSelected,
        editQuestion,
        saveQuestionSucceeded,
        saveQuestion,
        deleteQuestionSucceeded,
        deleteQuestion,
        swapQuestionOrdinals,
        moveQuestionUp,
        moveQuestionDown,
        displayMultipleChoiceOptions,
        refreshMultipleChoiceOptionsDisplay,
        saveMultipleChoiceOptionSucceeded,
        saveMultipleChoiceOption,
        createMultipleChoiceOption,
        deleteMultipleChoiceOptionSucceeded,
        deleteMultipleChoiceOption,
        displayRulesets,
        refreshRulesetsDisplay,
        saveRulesetSucceeded,
        saveRuleset,
        createRuleset,
        deleteRulesetSucceeded,
        confirmDeleteRuleset,
        deleteRuleset,
        swapRulesetOrdinals,
        moveRulesetUp,
        moveRulesetDown,
        addRule,
        editRule,
        ruleTypeSelected,
        saveRuleSucceeded,
        saveRule,
        deleteRuleSucceeded,
        confirmDeleteRule,
        deleteRule,
        updateRuleOrdinal,
        swapRuleOrdinals,
        moveRuleUp,
        moveRuleDown,
        displayRuleTiersLoadedSucceeded,
        refreshRuleTiersDisplay,
        saveRuleTierSucceeded,
        saveRuleTier,
        createRuleTier,
        editRuleTier,
        saveRuleTierOrdinal,
        swapRuleTierOrdinals,
        moveRuleTierUp,
        moveRuleTierDown,
        deleteRuleTierSucceeded,
        confirmDeleteRuleTier,
        deleteRuleTier,
        init
    };
} else {
    window.onload = init();
}

