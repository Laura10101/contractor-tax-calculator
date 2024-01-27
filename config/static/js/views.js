/*
 * views.js
 * Provides view functions to render views and react to view actions
 */
const { 
    dialogStates,
    statusDialog,
    confirmationDialog,
    jurisdictionsSelect,
    questionTypeDialog,
    booleanQuestionDialog,
    numericQuestionDialog,
    multipleChoiceQuestionDialog,
    multipleChoiceOptionDialog,
    questionDisplayContainer,
    booleanQuestionDisplay,
    numericQuestionDisplay,
    multipleChoiceQuestionDisplay,
    rulesetDialog,
    ruleTypeDialog,
    flatRateRuleDialog,
    tieredRateRuleDialog,
    secondaryTieredRateRuleDialog,
    ruleTierDialog,
    secondaryRuleTierDialog,
    rulesetsDisplayContainer,
    rulesetDisplay,
    flatRateRuleDisplay,
    tieredRateRuleDisplay,
    secondaryTieredRateRuleDisplay
 } = require("./view_consts.js");

const {
    queryToString,
    toUrl,
    getJurisdictions,
    getTaxCategories,
    getFormForJurisdiction,
    createBooleanQuestion,
    updateBooleanQuestion,
    createNumericQuestion,
    updateNumericQuestion,
    createMultipleChoiceQuestion,
    updateMultipleChoiceQuestion,
    updateQuestion,
    removeQuestion,
    postMultipleChoiceOption,
    removeMultipleChoiceOption,
    getRulesetsForJurisdiction,
    postRuleset,
    patchRuleset,
    removeRuleset,
    createFlatRateRule,
    updateFlatRateRule,
    createTieredRateRule,
    updateTieredRateRule,
    createSecondaryTieredRateRule,
    updateSecondaryTieredRateRule,
    removeRule,
    postRuleTier,
    updateRuleTier,
    removeRuleTier,
    postSecondaryRuleTier,
    updateSecondaryRuleTier,
    removeSecondaryRuleTier
} = require("./service_clients.js");

const {
    app,
    getFormId,
    findQuestionById,
    findRuleById,
    findParentRuleset,
    moveAppStateToParentState,
    moveParentStateToAppState,
    clearDialogState,
    clearParentState,
    setDialogState,
    setParentState,
    setParentRuleset,
    getTieredRateRulesForJurisdiction,
    resequenceQuestionOrdinals,
    resequenceRuleOrdinals,
    resequenceRulesetOrdinals,
    resequenceRuleTierOrdinals,
    findNextQuestion,
    findPreviousQuestion,
    findNextRuleset,
    findPreviousRuleset,
    findNextRule,
    findPreviousRule,
    findNextRuleTier,
    findPreviousRuleTier
} = require("./view_models.js");

const {
    showDialog,
    hideDialog,
    error,
    success,
    confirm,
    removeAllChildNodes,
    updateRuleTierTable,
    resetContainer,
    initJurisdictionsSelect,
    getSelectedJurisdictionId,
    displayCreateBooleanQuestionDialog,
    displayEditBooleanQuestionDialog,
    displayCreateNumericQuestionDialog,
    displayEditNumericQuestionDialog,
    updateMultipleChoiceQuestionDialogOptionsDisplay,
    displayCreateMultipleChoiceQuestionDialog,
    displayEditMultipleChoiceQuestionDialog,
    displayCreateMultipleChoiceOptionDialog,
    displayBooleanQuestion,
    displayNumericQuestion,
    displayMultipleChoiceQuestion,
    updateQuestionDisplay,
    displayCreateRulesetDialog,
    ruleTypeChosen,
    displayCreateFlatRateRuleDialog,
    displayEditFlatRateRuleDialog,
    displayCreateTieredRateRuleDialog,
    displayEditTieredRateRuleDialog,
    initPrimaryRulesSelect,
    displayCreateSecondaryTieredRateRuleDialog,
    displayEditSecondaryTieredRateRuleDialog,
    displayCreateRuleTierDialog,
    displayEditRuleTierDialog,
    initPrimaryRuleTiersSelect,
    displayCreateSecondaryRuleTierDialog,
    displayEditSecondaryRuleTierDialog,
    displayFlatRateRule,
    displayTieredRateRule,
    displaySecondaryTieredRateRule,
    displayRuleset,
    updateRulesetsDisplay
} = require("./view_utils.js");

function doNothing() {}
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
function refreshQuestionsDisplay(refresher=getFormForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayQuestions, displayQuestionsLoadError);
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

function saveQuestionSucceeded(refresher=refreshQuestionsDisplay) {
    success("The question was successfully saved.");
    clearDialogState();
    refresher();
}

function saveQuestionFailed(request, status, message) {
    error("An error occurred while attempting to save question.");
}

function saveQuestion(booleanQuestionCreator=createBooleanQuestion, numericQuestionCreator=createNumericQuestion,
    multipleChoiceQuestionCreator=createMultipleChoiceQuestion, booleanQuestionUpdater=updateBooleanQuestion, numericQuestionUpdater=updateNumericQuestion,
    multipleChoiceQuestionUpdater=updateMultipleChoiceQuestion) {
    formId = getFormId();

    if (app.dialogState.mode == dialogStates.modes.create) {
        switch (app.dialogState.entityType) {
            // Create boolean question
            case dialogStates.entityTypes.booleanQuestion:
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
                break;
            // Create numeric question
            case dialogStates.entityTypes.numericQuestion:
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
                    )
                break;
            // Create multiple choice questions
            case dialogStates.entityTypes.multipleChoiceQuestion:
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
                    )
                break;
        }
        
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        question = app.dialogState.entity;

        switch(app.dialogState.entityType) {
            // Edit boolean question
            case dialogStates.entityTypes.booleanQuestion:
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
                    )
                break;
            // Edit numeric question
            case dialogStates.entityTypes.numericQuestion:
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
                break;
            // Edit multiple choice question
            case dialogStates.entityTypes.multipleChoiceQuestion:
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
                    )
                break;
        }
    } else {
        error("Invalid dialog mode " + app.dialogState.mode + " found when saving question.");
    }
}

function deleteQuestionSucceeded(request, status, message, ordinalUpdater=updateQuestion, displayRefresher=refreshQuestionsDisplay) {
    success("The selected question was successfully deleted.");
    questions = resequenceQuestionOrdinals(app.dialogState.entity);
    questions.forEach(question => {
        if (question.id != app.dialogState.entity.id) {
            ordinalUpdater(question, doNothing, saveQuestionFailed);
        }
    })
    clearDialogState();
    displayRefresher();
}

function deleteQuestionFailed(request, status, message) {
    error("An error occurred while attempting to delete question.");
}

function confirmDeleteQuestion(remover=removeQuestion) {
    hideDialog(confirmationDialog.dialog.id);
    formId = getFormId();
    question = app.dialogState.entity;
    remover(formId, question.id, deleteQuestionSucceeded, deleteQuestionFailed);
}

function deleteQuestion(question) {
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.question, question);
    confirm("Please confirm you wish for the following question to be deleted: " + question.text + ".", confirmDeleteQuestion);
}

function swapQuestionOrdinals(question, findNewPosition, updater, refresher) {
    // Find the question that needs to be swapped
    let questionToSwap = findNewPosition(question);

    if (questionToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = question.ordinal;
        question.ordinal = questionToSwap.ordinal;
        questionToSwap.ordinal = originalOrdinal;

        // Save the questions
        updater(question, doNothing, saveQuestionFailed);
        updater(questionToSwap, doNothing, saveQuestionFailed);

        // Refresh the question display
        refresher();
    }
}

function moveQuestionUp(question, updater=updateQuestion, refresher=refreshQuestionsDisplay) {
    swapQuestionOrdinals(question, findPreviousQuestion, updater, refresher);
}

function moveQuestionDown(question, updater=updateQuestion, refresher=refreshQuestionsDisplay) {
    swapQuestionOrdinals(question, findNextQuestion, updater, refresher);
}

/*
 * Multiple Choice Option Views
 */
function displayMultipleChoiceOptions(data) {
    app.jurisdictionForm = data;

    if (app.parentState.entity != null) {
        if (app.parentState.entityType == dialogStates.entityTypes.multipleChoiceQuestion) {
            moveParentStateToAppState();
        }
    }

    question = findQuestionById(app.dialogState.entity.id);
    options = question.options;
    updateMultipleChoiceQuestionDialogOptionsDisplay(options);    
}

function displayMultipleChoiceOptionsError(request, status, message) {
    error("An error occurred while refreshing multiple choice options for question " + app.dialogState.entity.name);
}

function refreshMultipleChoiceOptionsDisplay(refresher=getFormForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayMultipleChoiceOptions, displayMultipleChoiceOptionsError);
}

function saveMultipleChoiceOptionSucceeded(refresher=refreshMultipleChoiceOptionsDisplay) {
    success("The option was successfully saved.");
    moveParentStateToAppState();
    refresher();
}

function saveMultipleChoiceOptionFailed(request, status, message) {
    error("An error occurred while attempting to save multiple choice option.");
}

function saveMultipleChoiceOption(creator=postMultipleChoiceOption) {
    hideDialog(multipleChoiceOptionDialog.dialog.id);

    formId = getFormId();
    questionId = app.parentState.entity.id;
    name = document.getElementById(multipleChoiceOptionDialog.name.input.id).value;
    explainer = document.getElementById(multipleChoiceOptionDialog.explainer.input.id).value;

    if (app.dialogState.mode == dialogStates.modes.create) {
        creator(formId, questionId, name, explainer, saveMultipleChoiceOptionSucceeded, saveMultipleChoiceOptionFailed);
    }
}

function createMultipleChoiceOption() {
    moveAppStateToParentState();
    setDialogState(dialogStates.modes.create, dialogStates.entityTypes.multipleChoiceOption, null);
    displayCreateMultipleChoiceOptionDialog();
}

function deleteMultipleChoiceOptionSucceeded(request, status, message, displayRefresher=refreshMultipleChoiceOptionsDisplay) {
    showDialog(multipleChoiceQuestionDialog.dialog.id);
    displayRefresher();
}

function deleteMultipleChoiceOptionFailed(request, status, message) {
    error("An error occurred while attempting to delete option.");
    moveParentStateToAppState();
    clearParentState();
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

function confirmDeleteMultipleChoiceOption(remover=removeMultipleChoiceOption) {
    hideDialog(confirmationDialog.dialog.id);
    formId = getFormId();
    question = app.parentState.entity;
    option = app.dialogState.entity;
    remover(formId, question.id, option.id, deleteMultipleChoiceOptionSucceeded, deleteMultipleChoiceOptionFailed);
}

function deleteMultipleChoiceOption(option) {
    moveAppStateToParentState();
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.multipleChoiceOption, option);
    hideDialog(multipleChoiceQuestionDialog.dialog.id);
    confirm("Please confirm you wish for the following option to be deleted: " + option.text + ".", confirmDeleteMultipleChoiceOption);
}

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

function refreshRulesetsDisplay(refresher=getRulesetsForJurisdiction) {
    jurisdictionId = getSelectedJurisdictionId();
    refresher(jurisdictionId, displayRulesets, displayRulesetsLoadError);
}

function saveRulesetSucceeded(refresher=refreshRulesetsDisplay) {
    success("The ruleset was successfully saved.");
    clearDialogState();
    refresher();
}

function saveRulesetFailed(request, status, message) {
    error("An error occurred while attempting to save ruleset.");
}

function saveRuleset(creator=postRuleset) {
    hideDialog(rulesetDialog.dialog.id);

    jurisdictionId = getSelectedJurisdictionId();
    taxCategoryId = document.getElementById(rulesetDialog.taxCategory.input.id).value;
    ordinal = getNextRulesetOrdinal();

    if (app.dialogState.mode == dialogStates.modes.create) {
        creator(jurisdictionId, taxCategoryId, ordinal, saveRulesetSucceeded, saveRulesetFailed);
    }
}

function createRuleset() {
    setDialogState(dialogStates.modes.create, dialogStates.entityTypes.ruleset, null);
    displayCreateRulesetDialog();
}

function deleteRulesetSucceeded(ordinalUpdater=patchRuleset, displayRefresher=refreshRulesetsDisplay) {
    success("The selected ruleset was successfully deleted.");
    rulesets = resequenceRulesetOrdinals(app.dialogState.entity);
    rulesets.forEach(ruleset => {
        if (ruleset.id != app.dialogState.entity.id) {
            ordinalUpdater(
                ruleset.id,
                ruleset.ordinal,
                doNothing,
                saveRulesetFailed);
        }
    });
    clearDialogState();
    displayRefresher();
}

function deleteRulesetFailed() {
    error("An error occurred while attempting to delete ruleset.");
}

function confirmDeleteRuleset(remover=removeRuleset) {
    hideDialog(confirmationDialog.dialog.id);
    remover(app.dialogState.entity.id, deleteRulesetSucceeded, deleteRulesetFailed);
}

function deleteRuleset(ruleset) {
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleset, ruleset);
    confirm("Please confirm you wish for the following ruleset to be deleted: " + ruleset.name + ".", confirmDeleteRuleset);
}

function swapRulesetOrdinals(ruleset, findNewPosition, updater, refresher) {
    // Find the question that needs to be swapped
    let rulesetToSwap = findNewPosition(ruleset);

    if (rulesetToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = ruleset.ordinal;
        ruleset.ordinal = rulesetToSwap.ordinal;
        rulesetToSwap.ordinal = originalOrdinal;

        // Save the questions
        updater(ruleset.id, ruleset.ordinal, doNothing, saveRulesetFailed);
        updater(rulesetToSwap.id, rulesetToSwap.ordinal, doNothing, saveRulesetFailed);

        // Refresh the question display
        refresher();
    }
}

function moveRulesetUp(ruleset, updater=patchRuleset, refresher=refreshRulesetsDisplay) {
    swapRulesetOrdinals(ruleset, findPreviousRuleset, updater, refresher);
}

function moveRulesetDown(ruleset, updater=patchRuleset, refresher=refreshRulesetsDisplay) {
    swapRulesetOrdinals(ruleset, findNextRuleset, updater, refresher);
}

/*
 * Rule Views
 */
function addRule(ruleset) {
    setParentRuleset(ruleset);
    showDialog(ruleTypeDialog.dialog.id);
}

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

function saveRuleSucceeded(refresher=refreshRulesetsDisplay) {
    success("The rule was successfully saved.");
    clearDialogState();
    refresher();
}

function saveRuleFailed(request, status, message) {
    error("An error occurred while attempting to save rule.");
}

function saveRule(flatRateRuleCreator=createFlatRateRule, tieredRateRuleCreator=createTieredRateRule,
    secondaryTieredRateRuleCreator=createSecondaryTieredRateRule, flatRateRuleUpdater=updateFlatRateRule, tieredRateRuleUpdater=updateTieredRateRule,
    secondaryTieredRateRuleUpdater=updateSecondaryTieredRateRule) {
    rulesetId = app.parentRuleset.id;

    if (app.dialogState.mode == dialogStates.modes.create) {
        switch (app.dialogState.entityType) {
            // Create flat rate rule
            case dialogStates.entityTypes.flatRateRule:
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
                    )
                break;
            // Create tiered rate rule
            case dialogStates.entityTypes.tieredRateRule:
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
                break;
            // Create secondary tiered rate rule
            case dialogStates.entityTypes.secondaryTieredRateRule:
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
                break;
        }
        
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        rule = app.dialogState.entity;
        switch(app.dialogState.entityType) {
            // Edit flat rate rule
            case dialogStates.entityTypes.flatRateRule:
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
                break;
            // Edit tiered rate rule
            case dialogStates.entityTypes.tieredRateRule:
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
                break;
            // Edit secondary tiered rate rule
            case dialogStates.entityTypes.secondaryTieredRateRule:
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
                break;
        }
    } else {
        error("Invalid dialog mode " + app.dialogState.mode + " found when saving question.");
    }
}

function deleteRuleSucceeded(flatRateRuleUpdater=updateFlatRateRule, tieredRateRuleUpdater=updateTieredRateRule,
    secondaryTieredRateRuleUpdater=updateSecondaryTieredRateRule, displayRefresher=refreshRulesetsDisplay) {

    success("The selected rule was successfully deleted.");
    rules = resequenceRuleOrdinals(app.dialogState.entity);
    rules.forEach(rule => {
        if (rule.id != app.dialogState.entity.id) {
            switch(rule.type) {
                case "flat_rate":
                        flatRateRuleUpdater(
                            app.parentRuleset.id,
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
                        tieredRateRuleUpdater(
                            app.parentRuleset.id,
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
                        if (rule.primary_rule.id != app.dialogState.entity.id) {
                            secondaryTieredRateRuleUpdater(
                                app.parentRuleset.id,
                                rule.id,
                                rule.name,
                                rule.explainer,
                                rule.variable_name,
                                rule.ordinal,
                                rule.primary_rule.id,
                                doNothing,
                                saveRuleFailed
                            );
                        }
                    break;
            }
        }
    });
    clearDialogState();
    displayRefresher();
}

function deleteRuleFailed() {
    error("An error occurred while attempting to delete rule.");
}

function confirmDeleteRule(remover=removeRule) {
    hideDialog(confirmationDialog.dialog.id);
    remover(app.parentRuleset.id, app.dialogState.entity.id, deleteRuleSucceeded, deleteRuleFailed);
}

function deleteRule(ruleset, rule) {
    setParentRuleset(ruleset);
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.rule, rule);
    confirm("Please confirm you wish for the following rule to be deleted: " + rule.name + ".", confirmDeleteRule);
}

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

function swapRuleOrdinals(ruleset, rule, findNewPosition, updater, refresher) {
    // Find the rule that needs to be swapped
    let ruleToSwap = findNewPosition(ruleset, rule);

    if (ruleToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = rule.ordinal;
        rule.ordinal = ruleToSwap.ordinal;
        ruleToSwap.ordinal = originalOrdinal;

        // Save the ordinals
        updater(ruleset, rule);
        updater(ruleset, ruleToSwap);

        // Refresh the ruleset display
        refresher();
    }
}

function moveRuleUp(ruleset, rule, updater=updateRuleOrdinal, refresher=refreshRulesetsDisplay) {
    swapRuleOrdinals(ruleset, rule, findPreviousRule, updater, refresher);
}

function moveRuleDown(ruleset, rule, updater=updateRuleOrdinal, refresher=refreshRulesetsDisplay) {
    swapRuleOrdinals(ruleset, rule, findNextRule, updater, refresher);
}

/*
 * Rule Tier Views
 */
function displayRuleTiersLoadedSucceeded(data) {
    app.jurisdictionRules = data;

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

function saveRuleTierSucceeded(refresher=refreshRuleTiersDisplay) {
    success("The tier was successfully saved.");
    moveParentStateToAppState();
    refresher();
}

function saveRuleTierFailed(request, status, message) {
    error("An error occurred while attempting to save rule tier.");
}

function saveRuleTier(ruleTierCreator=postRuleTier, secondaryRuleTierCreator=postSecondaryRuleTier, ruleTierUpdater=updateRuleTier,
    secondaryRuleTierUpdater=updateSecondaryRuleTier) {
    rule = app.parentState.entity;
    ruleset = findParentRuleset(rule.id);

    if (app.dialogState.mode == dialogStates.modes.create)
    {
        switch (app.dialogState.entityType) {
            case dialogStates.entityTypes.ruleTier:
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
                break;
            case dialogStates.entityTypes.secondaryRuleTier:
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
                break;
        }
    } else if (app.dialogState.mode == dialogStates.modes.edit) {
        tier = app.dialogState.entity;
        switch (app.dialogState.entityType) {
            case dialogStates.entityTypes.ruleTier:
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
                break;
            case dialogStates.entityTypes.secondaryRuleTier:
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
        updater(swapPrimary, tier);
        updater(swapPrimary, tierToSwap);

        refresher();
    }
}

function moveRuleTierUp(isPrimary, tier, updater=saveRuleTierOrdinal, refresher=refreshRuleTiersDisplay) {
    swapRuleTierOrdinals(isPrimary, tier, findPreviousRuleTier, updater, refresher);
}

function moveRuleTierDown(isPrimary, tier, updater=saveRuleTierOrdinal, refresher=refreshRuleTiersDisplay) {
    swapRuleTierOrdinals(isPrimary, tier, findNextRuleTier, updater, refresher);
}

function deleteRuleTierSucceeded(primaryTierUpdater=updateRuleTier, secondaryTierUpdater=updateSecondaryRuleTier, displayRefresher=refreshRuleTiersDisplay) {
    success("The selected rule tier was successfully deleted.");
    rule = app.parentState.entity;
    ruleset = findParentRuleset(rule.id);

    tiers = resequenceRuleTierOrdinals(app.dialogState.entity);
    tiers.forEach(tier => {
        if (tier.id != app.dialogState.entity.id) {
            switch(app.dialogState.entityType) {
                case dialogStates.entityTypes.ruleTier:
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
                    break;
                case dialogStates.entityTypes.secondaryRuleTier:
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
                    break;
            }
        }
    });
    moveParentStateToAppState();
    displayRefresher();
}

function deleteRuleTierFailed(request, status, message) {
    error("An error occurred while attempting to delete rule tier.");
    moveParentStateToAppState();
}

function confirmDeleteRuleTier(primaryRemover=removeRuleTier, secondaryRemover=removeSecondaryRuleTier) {
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
        setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleTier, tier);
    } else {
        setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.secondaryRuleTier, tier);
    }
    confirm("Please confirm you wish for the selected rule tier to be deleted.", confirmDeleteRuleTier);
}

/*
 * Initialisation functions
 */
function init() {
    setApiHost(window.location.protocol, window.location.hostname);
    getJurisdictions(loadJurisdictionSelect, displayJurisdictionLoadError);
    getTaxCategories(loadTaxCategorySelect, displayTaxCategoryLoadError);
}

if (module == undefined) {
    window.onload = init();
} else {
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
}

