/*
 * views.js
 * Provides view functions to render views and react to view actions
 */

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
                    createNumericQuestion(
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
                    createMultipleChoiceQuestion(
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

function deleteQuestionSucceeded(request, status, message) {
    success("The selected question was successfully deleted.");
    questions = resequenceQuestionOrdinals(app.dialogState.entity);
    questions.forEach(question => {
        updateQuestion(question, doNothing, saveQuestionFailed);
    })
    clearDialogState();
    refreshQuestionsDisplay();
}

function deleteQuestionFailed(request, status, message) {
    error("An error occurred while attempting to save question.");
}

function confirmDeleteQuestion() {
    hideDialog(confirmationDialog.dialog.id);
    formId = getFormId();
    question = app.dialogState.entity;
    removeQuestion(formId, question.id, deleteQuestionSucceeded, deleteQuestionFailed);
}

function deleteQuestion(question) {
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.question, question);
    confirm("Please confirm you wish for the following question to be deleted: " + question.text + ".", confirmDeleteQuestion);
}

function swapQuestionOrdinals(question, findNewPosition) {
    // Find the question that needs to be swapped
    let questionToSwap = findNewPosition(question);

    if (questionToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = question.ordinal;
        question.ordinal = questionToSwap.ordinal;
        questionToSwap.ordinal = originalOrdinal;

        // Save the questions
        updateQuestion(question, doNothing, saveQuestionFailed);
        updateQuestion(questionToSwap, doNothing, saveQuestionFailed);

        // Refresh the question display
        refreshQuestionsDisplay();
    }
}

function moveQuestionUp(question) {
    swapQuestionOrdinals(question, findPreviousQuestion);
}

function moveQuestionDown(question) {
    swapQuestionOrdinals(question, findNextQuestion);
}

/*
 * Multiple Choice Option Views
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

function refreshRulesetsDisplay() {
    jurisdictionId = getSelectedJurisdictionId();
    getRulesetsForJurisdiction(jurisdictionId, displayRulesets, displayRulesetsLoadError);
}

function saveRulesetSucceeded() {
    success("The ruleset was successfully saved.");
    clearDialogState();
    refreshRulesetsDisplay();
}

function saveRulesetFailed(request, status, message) {
    error("An error occurred while attempting to save ruleset.");
}

function saveRuleset() {
    hideDialog(rulesetDialog.dialog.id);

    jurisdictionId = getSelectedJurisdictionId();
    taxCategoryId = document.getElementById(rulesetDialog.taxCategory.input.id).value;
    ordinal = getNextRulesetOrdinal();

    if (app.dialogState.mode == dialogStates.modes.create) {
        postRuleset(jurisdictionId, taxCategoryId, ordinal, saveRulesetSucceeded, saveRulesetFailed);
    }
}

function createRuleset() {
    setDialogState(dialogStates.modes.create, dialogStates.entityTypes.ruleset, null);
    displayCreateRulesetDialog();
}

function deleteRulesetSucceeded() {
    success("The selected ruleset was successfully deleted.");
    rulesets = resequenceRulesetOrdinals(app.dialogState.entity);
    rulesets.forEach(ruleset => {
        if (ruleset.id != app.dialogState.entity.id) {
            patchRuleset(
                ruleset.id,
                ruleset.ordinal,
                doNothing,
                saveRulesetFailed);
        }
    });
    clearDialogState();
    refreshRulesetsDisplay();
}

function deleteRulesetFailed() {
    error("An error occurred while attempting to delete ruleset.");
}

function confirmDeleteRuleset() {
    hideDialog(confirmationDialog.dialog.id);
    removeRuleset(app.dialogState.entity.id, deleteRulesetSucceeded, deleteRulesetFailed);
}

function deleteRuleset(ruleset) {
    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleset, ruleset);
    confirm("Please confirm you wish for the following ruleset to be deleted: " + ruleset.name + ".", confirmDeleteRuleset);
}

function swapRulesetOrdinals(ruleset, findNewPosition) {
    // Find the question that needs to be swapped
    let rulesetToSwap = findNewPosition(ruleset);

    if (rulesetToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = ruleset.ordinal;
        ruleset.ordinal = rulesetToSwap.ordinal;
        rulesetToSwap.ordinal = originalOrdinal;

        // Save the questions
        patchRuleset(ruleset.id, ruleset.ordinal, doNothing, saveRulesetFailed);
        patchRuleset(rulesetToSwap.id, rulesetToSwap.ordinal, doNothing, saveRulesetFailed);

        // Refresh the question display
        refreshRulesetsDisplay();
    }
}

function moveRulesetUp(ruleset) {
    swapRulesetOrdinals(ruleset, findPreviousRuleset);
}

function moveRulesetDown(ruleset) {
    swapRulesetOrdinals(ruleset, findNextRuleset);
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

function saveRuleSucceeded() {
    success("The rule was successfully saved.");
    clearDialogState();
    refreshRulesetsDisplay();
}

function saveRuleFailed(request, status, message) {
    error("An error occurred while attempting to save rule.");
}

function saveRule() {
    rulesetId = app.parentRuleset.id;

    if (app.dialogState.mode == dialogStates.modes.create) {
        switch (app.dialogState.entityType) {
            // Create flat rate rule
            case dialogStates.entityTypes.flatRateRule:
                    hideDialog(flatRateRuleDialog.dialog.id);
                    createFlatRateRule(
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
                    createTieredRateRule(
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
                    createSecondaryTieredRateRule(
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
                    updateFlatRateRule(
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
                    updateTieredRateRule(
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
                    updateSecondaryTieredRateRule(
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

function deleteRuleSucceeded() {
    success("The selected rule was successfully deleted.");
    rules = resequenceRuleOrdinals(app.dialogState.entity);
    rules.forEach(rule => {
        if (rule.id != app.dialogState.entity.id) {
            switch(rule.type) {
                case "flat_rate":
                        updateFlatRateRule(
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
                        updateTieredRateRule(
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
                            updateSecondaryTieredRateRule(
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
    refreshRulesetsDisplay();
}

function deleteRuleFailed() {
    error("An error occurred while attempting to delete rule.");
}

function confirmDeleteRule() {
    hideDialog(confirmationDialog.dialog.id);
    removeRule(app.parentRuleset.id, app.dialogState.entity.id, deleteRuleSucceeded, deleteRuleFailed);
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

function swapRuleOrdinals(ruleset, rule, findNewPosition) {
    // Find the rule that needs to be swapped
    let ruleToSwap = findNewPosition(ruleset, rule);

    if (ruleToSwap != null) {
        // Swap the ordinals
        let originalOrdinal = rule.ordinal;
        rule.ordinal = ruleToSwap.ordinal;
        ruleToSwap.ordinal = originalOrdinal;

        // Save the ordinals
        updateRuleOrdinal(ruleset, rule);
        updateRuleOrdinal(ruleset, ruleToSwap);

        // Refresh the ruleset display
        refreshRulesetsDisplay();
    }
}

function moveRuleUp(ruleset, rule) {
    swapRuleOrdinals(ruleset, rule, findPreviousRule);
}

function moveRuleDown(ruleset, rule) {
    swapRuleOrdinals(ruleset, rule, findNextRule);
}

/*
 * Initialisation functions
 */
function init() {
    getJurisdictions(loadJurisdictionSelect, displayJurisdictionLoadError);
    getTaxCategories(loadTaxCategorySelect, displayTaxCategoryLoadError);
}

window.onload = init();