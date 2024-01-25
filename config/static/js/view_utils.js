const $ = require("jquery");
require("bootstrap");
const {
    dialogStates,
    endpoints,
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
    resequenceRuleTierOrdinals
} = require("./view_models.js");
/*
 * General Helper Functions
 */

function showMessage(message) {
    document.getElementById(statusDialog.message.id).innerHTML = message;
    showDialog(statusDialog.dialog.id);
}

function error(message) {
    showMessage(message);
}

function success(message) {
    showMessage(message);
}

function confirm(message, onConfirm) {
    document.getElementById(confirmationDialog.message.id).innerHTML = message;
    document.getElementById(confirmationDialog.confirmationButton.id).onclick = onConfirm;
    showDialog(confirmationDialog.dialog.id);
}

// Remove all child nodes of a parent DOM element
// Taken from https://www.javascripttutorial.net/dom/manipulating/remove-all-child-nodes/
function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function showDialog(dialogId) {
    $("#" + dialogId).modal("show");
}

function hideDialog(dialogId) {
    $("#" + dialogId).modal("hide");
}

function updateRuleTierTable(updatePrimary, tiers) {
    // Get the row
    if (updatePrimary) {
        table = document.getElementById(tieredRateRuleDialog.tiers.table.id);
        prototypeRow = document.getElementById(tieredRateRuleDialog.tiers.tierRow.id);
    } else {
        table = document.getElementById(secondaryTieredRateRuleDialog.tiers.table.id);
        prototypeRow = document.getElementById(secondaryTieredRateRuleDialog.tiers.tierRow.id);
    }
    removeAllChildNodes(table);

    // Add prototype row back in so it's available next time
    table.appendChild(prototypeRow);

    // Display one row for each tier
    tiers.forEach(tier => {
        tierRow = prototypeRow.cloneNode(true);

        // Update IDs to avoid duplicates
        tierRow.id += "-" + tier.id;
        tierRow.classList.remove("hidden");
        tierRow.firstChild.id += "-" + tier.id;

        // Update tier data in display
        if (updatePrimary) {
            tierRow.children[0].innerHTML = tier.min_value;
            tierRow.children[1].innerHTML = tier.max_value;
            tierRow.children[2].innerHTML = tier.tier_rate;
        } else {
            primaryTier = findPrimaryRuleTierById(tier.primary_tier_id);
            tierRow.children[0].innerHTML = primaryTier.min_value;
            tierRow.children[1].innerHTML = primaryTier.max_value;
            tierRow.children[2].innerHTML = tier.tier_rate;
        }

        // Add event handlers to tier actions
        tierRow.querySelector(".edit-button").onclick = function() { editRuleTier(updatePrimary, tier); }
        tierRow.querySelector(".delete-button").onclick = function() { deleteRuleTier(updatePrimary, tier); }
        tierRow.querySelector(".move-up-button").onclick = function() { moveRuleTierUp(updatePrimary, tier); }
        tierRow.querySelector(".move-down-button").onclick = function() { moveRuleTierDown(updatePrimary, tier); }

        // Add the new row
        table.appendChild(tierRow);
    });
}

function resetContainer(containerId, prototypeIds) {
    prototypes = {};
    prototypeIds.forEach(prototypeId => {
        prototypes[prototypeId] = document.getElementById(prototypeId);
    });

    container = document.getElementById(containerId);
    removeAllChildNodes(container);

    for (const prototypeId in prototypes) {
        container.appendChild(prototypes[prototypeId]);
    }
}

/*
 * Jurisdiction Select Helper Functions
 */

// Display a list of jurisdictions in the jurisdictions select and set the onChange callback
function initJurisdictionsSelect(jurisdictions, selectionChangedCallback) {
    // Get the jurisdictions select box
    select = document.getElementById(jurisdictionsSelect.id);

    // Display only jurisdictions from the new list in the select box
    removeAllChildNodes(select);
    jurisdictions.forEach(jurisdiction => {
            jurisdictionOption = document.createElement("option");
            jurisdictionOption.text = jurisdiction.name;
            jurisdictionOption.value = jurisdiction.id;
            select.add(jurisdictionOption);
    });

    // Set onChange callback function
    select.addEventListener("change", selectionChangedCallback);
}

function getSelectedJurisdictionId() {
    return document.getElementById(jurisdictionsSelect.id).value;
}

/*
 * Question Dialog Helper Functions
 */

// Boolean Question Dialog Helpers

// Set the label and input values on a boolean question dialog
function initBooleanQuestionDialog(dialogLabel, questionText, explainer, variableName, isMandatory) {
    document.getElementById(booleanQuestionDialog.label.id).innerText = dialogLabel;
    document.getElementById(booleanQuestionDialog.questionText.input.id).value = questionText;
    document.getElementById(booleanQuestionDialog.explainer.input.id).value = explainer;
    document.getElementById(booleanQuestionDialog.variableName.input.id).value = variableName;
    document.getElementById(booleanQuestionDialog.isMandatory.input.id).checked = isMandatory;
}

// Set up and display a create question dialog
function displayCreateBooleanQuestionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initBooleanQuestionDialog("Create Boolean Question", "", "", "", false);
    // Show the dialog
    showDialog(booleanQuestionDialog.dialog.id);
}

function displayEditBooleanQuestionDialog(question) {
    // Initialise the boolean question dialog with appropriate values for a create
    initBooleanQuestionDialog(
        "Edit Boolean Question",
        question.text,
        question.explainer,
        question.variable_name,
        question.is_mandatory
    );
    // Show the dialog
    showDialog(booleanQuestionDialog.dialog.id);
}


// Numeric Question Dialog Helpers
function initNumericQuestionDialog(dialogLabel, questionText, explainer, variableName, isMandatory, isInteger, minValue, maxValue) {
    document.getElementById(numericQuestionDialog.label.id).innerText = dialogLabel;
    document.getElementById(numericQuestionDialog.questionText.input.id).value = questionText;
    document.getElementById(numericQuestionDialog.explainer.input.id).value = explainer;
    document.getElementById(numericQuestionDialog.variableName.input.id).value = variableName;
    document.getElementById(numericQuestionDialog.isMandatory.input.id).checked = isMandatory;
    document.getElementById(numericQuestionDialog.isInteger.input.id).checked = isInteger;
    document.getElementById(numericQuestionDialog.minimumValue.input.id).value = minValue;
    document.getElementById(numericQuestionDialog.maximumValue.input.id).value = maxValue;
}

function displayCreateNumericQuestionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initNumericQuestionDialog("Create Numeric Question", "", "", "", false, false, "", "");
    // Show the dialog
    showDialog(numericQuestionDialog.dialog.id);
}

function displayEditNumericQuestionDialog(question) {
    initNumericQuestionDialog(
        "Edit Numeric Question",
        question.text,
        question.explainer,
        question.variable_name,
        question.is_mandatory,
        question.is_integer,
        question.min_value,
        question.max_value
    );
    // Show the dialog
    showDialog(numericQuestionDialog.dialog.id);
}

// Multiple Choice Question Dialog
function updateMultipleChoiceQuestionDialogOptionsDisplay(options) {
    // Get the row 
    optionsTable = document.getElementById(multipleChoiceQuestionDialog.options.table.id);
    prototypeOptionsRow = document.getElementById(multipleChoiceQuestionDialog.options.optionRow.id);
    removeAllChildNodes(optionsTable);

    // Add prototype row back in so it's available next time
    optionsTable.appendChild(prototypeOptionsRow);

    // Display one row for each option
    options.forEach(option => {
        optionRow = prototypeOptionsRow.cloneNode(true);

        // Update IDs to avoid duplicates
        optionRow.id += "-" + option.id;
        optionRow.classList.remove("hidden");
        optionRow.children[0].id += "-" + option.id;

        // Update option name in display
        optionRow.children[0].innerHTML = option.text;

        // Set delete button event handler
        optionRow.querySelector(".delete-button").onclick = function() { deleteMultipleChoiceOption(option); }

        // Add the new row
        optionsTable.appendChild(optionRow);
    });
}

function initMultipleChoiceQuestionDialog(dialogLabel, questionText, explainer, variableName, isMandatory, allowMultiselect, options) {
    document.getElementById(multipleChoiceQuestionDialog.label.id).innerText = dialogLabel;
    document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value = questionText;
    document.getElementById(multipleChoiceQuestionDialog.explainer.input.id).value = explainer;
    document.getElementById(multipleChoiceQuestionDialog.variableName.input.id).value = variableName;
    document.getElementById(multipleChoiceQuestionDialog.isMandatory.input.id).checked = isMandatory;
    document.getElementById(multipleChoiceQuestionDialog.allowMultiselect.input.id).checked = allowMultiselect;
    updateMultipleChoiceQuestionDialogOptionsDisplay(options);
}

function displayCreateMultipleChoiceQuestionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initMultipleChoiceQuestionDialog("Create Multiple Choice Question", "", "", "", false, false, []);
    // Show the dialog
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

function displayEditMultipleChoiceQuestionDialog(question) {
    // Initialise the boolean question dialog with appropriate values for a create
    initMultipleChoiceQuestionDialog(
        "Edit Multiple Choice Question",
        question.text,
        question.explainer,
        question.variable_name,
        question.is_mandatory,
        question.is_multiselect,
        question.options
    );
    // Show the dialog
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

/*
 * Multiple Choice Option Helper Functions
 */
function initMultipleChoiceOptionDialog(name, explainer) {
    document.getElementById(multipleChoiceOptionDialog.name.input.id).innerText = name;
    document.getElementById(multipleChoiceOptionDialog.explainer.input.id).value = explainer;
}

function displayCreateMultipleChoiceOptionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initMultipleChoiceOptionDialog("", "");
    // Show the dialog
    showDialog(multipleChoiceOptionDialog.dialog.id);
}


/*
 * Question Display Helper Functions
 */
function displayBooleanQuestion(question) {
    // Create a new question display for this question
    questionDisplay = document.getElementById(booleanQuestionDisplay.card.id).cloneNode(true);
    questionDisplay.classList.remove("hidden");
    questionDisplay.id += "-" + question.id;

    // Update the data
    questionTextDisplay = questionDisplay.querySelector("#" + booleanQuestionDisplay.questionText.id);
    questionTextDisplay.id += "-" + question.id;
    questionTextDisplay.innerHTML = question.text;

    questionVariableNameDisplay = questionDisplay.querySelector("#" + booleanQuestionDisplay.variableName.id);
    questionVariableNameDisplay.id += "-" + question.id;
    questionVariableNameDisplay.innerHTML = question.variable_name;

    questionExplainerDisplay = questionDisplay.querySelector("#" + booleanQuestionDisplay.explainer.id);
    questionExplainerDisplay.id += "-" + question.id;
    questionExplainerDisplay.innerHTML = question.explainer;

    questionMandatoryDisplay = questionDisplay.querySelector("#" + booleanQuestionDisplay.isMandatory.id);
    questionMandatoryDisplay.id += "-" + question.id;
    questionMandatoryDisplay.innerHTML = question.is_mandatory ? "Mandatory" : "Optional";
    
    // Set the action event handlers
    questionDisplay.querySelector(".edit-button").onclick = function() { editQuestion(question); }
    questionDisplay.querySelector(".delete-button").onclick = function() { deleteQuestion(question); }
    questionDisplay.querySelector(".move-up-button").onclick = function() { moveQuestionUp(question); }
    questionDisplay.querySelector(".move-down-button").onclick = function() { moveQuestionDown(question); }

    // Add the question display to the container
    document.getElementById(questionDisplayContainer.id).appendChild(questionDisplay);
}

function displayNumericQuestion(question) {
    questionDisplay = document.getElementById(numericQuestionDisplay.card.id).cloneNode(true);
    questionDisplay.classList.remove("hidden");
    questionDisplay.id += "-" + question.id;
    
    questionTextDisplay = questionDisplay.querySelector("#" + numericQuestionDisplay.questionText.id);
    questionTextDisplay.id += "-" + question.id;
    questionTextDisplay.innerHTML = question.text;

    questionVariableNameDisplay = questionDisplay.querySelector("#" + numericQuestionDisplay.variableName.id);
    questionVariableNameDisplay.id += "-" + question.id;
    questionVariableNameDisplay.innerHTML = question.variable_name;

    questionExplainerDisplay = questionDisplay.querySelector("#" + numericQuestionDisplay.explainer.id);
    questionExplainerDisplay.id += "-" + question.id;
    questionExplainerDisplay.innerHTML = question.explainer;

    questionMandatoryDisplay = questionDisplay.querySelector("#" + numericQuestionDisplay.isMandatory.id);
    questionMandatoryDisplay.id += "-" + question.id;
    questionMandatoryDisplay.innerHTML = question.is_mandatory ? "Mandatory" : "Optional";

    questionValidationSummaryDisplay = questionDisplay.querySelector("#" + numericQuestionDisplay.validationRuleSummary.id);
    questionValidationSummaryDisplay.id += "-" + question.id;
    questionValidationSummaryDisplay.innerHTML = question.is_integer ? "Integer" : "Decimal";
    questionValidationSummaryDisplay.innerHTML += " between " + question.min_value + " and " + question.max_value;

    // Set the action event handlers
    questionDisplay.querySelector(".edit-button").onclick = function() { editQuestion(question); }
    questionDisplay.querySelector(".delete-button").onclick = function() { deleteQuestion(question); }
    questionDisplay.querySelector(".move-up-button").onclick = function() { moveQuestionUp(question); }
    questionDisplay.querySelector(".move-down-button").onclick = function() { moveQuestionDown(question); }

    document.getElementById(questionDisplayContainer.id).appendChild(questionDisplay);
}

function displayMultipleChoiceQuestion(question) {
    questionDisplay = document.getElementById(multipleChoiceQuestionDisplay.card.id).cloneNode(true);
    questionDisplay.classList.remove("hidden");
    questionDisplay.id += "-" + question.id;
    
    questionTextDisplay = questionDisplay.querySelector("#" + multipleChoiceQuestionDisplay.questionText.id);
    questionTextDisplay.id += "-" + question.id;
    questionTextDisplay.innerHTML = question.text;

    questionVariableNameDisplay = questionDisplay.querySelector("#" + multipleChoiceQuestionDisplay.variableName.id);
    questionVariableNameDisplay.id += "-" + question.id;
    questionVariableNameDisplay.innerHTML = question.variable_name;

    questionExplainerDisplay = questionDisplay.querySelector("#" + multipleChoiceQuestionDisplay.explainer.id);
    questionExplainerDisplay.id += "-" + question.id;
    questionExplainerDisplay.innerHTML = question.explainer;

    questionMandatoryDisplay = questionDisplay.querySelector("#" + multipleChoiceQuestionDisplay.isMandatory.id);
    questionMandatoryDisplay.id += "-" + question.id;
    questionMandatoryDisplay.innerHTML = question.is_mandatory ? "Mandatory" : "Optional";

    questionMultiselectDisplay = questionDisplay.querySelector("#" + multipleChoiceQuestionDisplay.isMultiselect.id);
    questionMultiselectDisplay.id += "-" + question.id;
    questionMultiselectDisplay.innerHTML = question.is_multiselect ? "Allow multiple selections" : "Single selection only";  

    // Set the action event handlers
    questionDisplay.querySelector(".edit-button").onclick = function() { editQuestion(question); }
    questionDisplay.querySelector(".delete-button").onclick = function() { deleteQuestion(question); }
    questionDisplay.querySelector(".move-up-button").onclick = function() { moveQuestionUp(question); }
    questionDisplay.querySelector(".move-down-button").onclick = function() { moveQuestionDown(question); }

    document.getElementById(questionDisplayContainer.id).appendChild(questionDisplay);
}

function updateQuestionDisplay(questions) {
    resetContainer(questionDisplayContainer.id, [
        booleanQuestionDisplay.card.id,
        numericQuestionDisplay.card.id,
        multipleChoiceQuestionDisplay.card.id
    ]);

    questions.forEach(question => {
        switch (question.type) {
            case "boolean":
                    displayBooleanQuestion(question);
                break;
            case "numeric":
                    displayNumericQuestion(question);
                break;
            case "multiple_choice":
                    displayMultipleChoiceQuestion(question);
                break;
        }
    });
}

/*
 * Rule Dialog Helper Functions
 */
// Rule Type Dialog Helpers

// Ruleset Dialog Helpers
function initRulesetDialog(dialogLabel, taxCategories) {
    document.getElementById(rulesetDialog.label.id).innerText = dialogLabel;
    select = document.getElementById(rulesetDialog.taxCategory.input.id);
    removeAllChildNodes(select);
    taxCategories.forEach(category => {
        option = document.createElement("option");
        option.text = category.name;
        option.value = category.tax_category_id;
        select.add(option);
    });
}

function displayCreateRulesetDialog() {
    // Initialise the ruleset dialog with appropriate values for a create
    initRulesetDialog("Create Ruleset", app.taxCategories);
    // Show the dialog
    showDialog(rulesetDialog.dialog.id);
}

// Handle selection of a question type via question type modal
function ruleTypeChosen() {
    // Close the modal
    hideDialog(ruleTypeDialog.dialog.id);

    // Display the appropraite create question dialog for the selected question type
    ruleType = document.getElementById(ruleTypeDialog.ruleType.input.id).value;
    switch(ruleType) {
        case "flat_rate":
            displayCreateFlatRateRuleDialog();
        break;

        case "tiered_rate":
            displayCreateTieredRateRuleDialog();
        break;
        
        case "secondary_tiered_rate":
            displayCreateSecondaryTieredRateRuleDialog();
        break;
    }
}

// Flat Rate Rule Dialog Helpers
function initFlatRateRuleDialog(dialogLabel, name, explainer, variableName, taxRate) {
    document.getElementById(flatRateRuleDialog.label.id).innerText = dialogLabel;
    document.getElementById(flatRateRuleDialog.name.input.id).value = name;
    document.getElementById(flatRateRuleDialog.explainer.input.id).value = explainer;
    document.getElementById(flatRateRuleDialog.variableName.input.id).value = variableName;
    document.getElementById(flatRateRuleDialog.taxRate.input.id).value = taxRate;
}

function displayCreateFlatRateRuleDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initFlatRateRuleDialog("Create Flat Rate Rule", "", "", "", "");
    // Show the dialog
    showDialog(flatRateRuleDialog.dialog.id);
}

function displayEditFlatRateRuleDialog(rule) {
    initFlatRateRuleDialog(
        "Edit Flat Rate Rule",
        rule.name,
        rule.explainer,
        rule.variable_name,
        rule.tax_rate
    );
    // Show the dialog
    showDialog(flatRateRuleDialog.dialog.id);
}

// Tiered Rate Rule Dialog Helpers
function initTieredRateRuleDialog(dialogLabel, name, explainer, variableName, tiers) {
    document.getElementById(tieredRateRuleDialog.label.id).innerText = dialogLabel;
    document.getElementById(tieredRateRuleDialog.name.input.id).value = name;
    document.getElementById(tieredRateRuleDialog.explainer.input.id).value = explainer;
    document.getElementById(tieredRateRuleDialog.variableName.input.id).value = variableName;
    updateRuleTierTable(true, tiers);
}

function displayCreateTieredRateRuleDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initTieredRateRuleDialog("Create Tiered Rate Rule", "", "", "", []);
    // Show the dialog
    showDialog(tieredRateRuleDialog.dialog.id);
}

function displayEditTieredRateRuleDialog(rule) {
    initTieredRateRuleDialog(
        "Edit Tiered Rate Rule",
        rule.name,
        rule.explainer,
        rule.variable_name,
        rule.tiers
    );
    // Show the dialog
    showDialog(tieredRateRuleDialog.dialog.id);
}

// Secondary Tiered Rate Rule Dialog Helpers
function initPrimaryRulesSelect(rules) {
    select = document.getElementById(secondaryTieredRateRuleDialog.primaryRule.input.id);
    rules.forEach(rule => {
        option = document.createElement("option");
        option.text = rule.name;
        option.value = rule.id;
        select.add(option);
    });
}

function initSecondaryTieredRateRuleDialog(dialogLabel, name, explainer, variableName, primaryRules, tiers) {
    document.getElementById(secondaryTieredRateRuleDialog.label.id).innerText = dialogLabel;
    document.getElementById(secondaryTieredRateRuleDialog.name.input.id).value = name;
    document.getElementById(secondaryTieredRateRuleDialog.explainer.input.id).value = explainer;
    document.getElementById(secondaryTieredRateRuleDialog.variableName.input.id).value = variableName;
    initPrimaryRulesSelect(primaryRules);
    updateRuleTierTable(false, tiers);
}

function displayCreateSecondaryTieredRateRuleDialog(primaryRules) {
    // Initialise the boolean question dialog with appropriate values for a create
    initSecondaryTieredRateRuleDialog("Create Secondary Tiered Rate Rule", "", "", "", primaryRules, []);
    // Show the dialog
    showDialog(secondaryTieredRateRuleDialog.dialog.id);
}

function displayEditSecondaryTieredRateRuleDialog(rule, primaryRules) {
    initSecondaryTieredRateRuleDialog(
        "Edit Secondary Tiered Rate Rule",
        rule.name,
        rule.explainer,
        rule.variable_name,
        primaryRules,
        rule.tiers
    );
    // Show the dialog
    showDialog(secondaryTieredRateRuleDialog.dialog.id);
}

// Primary Rule Tier Dialog Helpers
function initRuleTierDialog(dialogLabel, minValue, maxValue, taxRate) {
    document.getElementById(ruleTierDialog.label.id).innerText = dialogLabel;
    document.getElementById(ruleTierDialog.minimumValue.input.id).value = minValue;
    document.getElementById(ruleTierDialog.maximumValue.input.id).value = maxValue;
    document.getElementById(ruleTierDialog.taxRate.input.id).value = taxRate;
}

function displayCreateRuleTierDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initRuleTierDialog("Create Primary Rule Tier", "", "", "");
    // Show the dialog
    showDialog(ruleTierDialog.dialog.id);
}

function displayEditRuleTierDialog(tier) {
    initRuleTierDialog(
        "Edit Primary Rule Tier",
        tier.min_value,
        tier.max_value,
        tier.tier_rate
    );
    // Show the dialog
    showDialog(ruleTierDialog.dialog.id);
}

// Secondary Rule Tier Dialog Helpers
function initPrimaryRuleTiersSelect(tiers) {
    select = document.getElementById(secondaryRuleTierDialog.primaryTier.input.id);
    tiers.forEach(tier => {
        option = document.createElement("option");
        option.text = tier.min_value + " - " + tier.max_value + " (" + tier.tier_rate + ")";
        option.value = tier.id;
        select.add(option);
    });
}

function initSecondaryRuleTierDialog(dialogLabel, primaryRuleTiers, taxRate) {
    document.getElementById(secondaryRuleTierDialog.label.id).innerText = dialogLabel;
    initPrimaryRuleTiersSelect(primaryRuleTiers);
    document.getElementById(secondaryRuleTierDialog.taxRate.input.id).value = taxRate;
}

function displayCreateSecondaryRuleTierDialog(primaryTiers) {
    // Initialise the boolean question dialog with appropriate values for a create
    initSecondaryRuleTierDialog("Create Secondary Rule Tier", primaryTiers, "");
    // Show the dialog
    showDialog(secondaryRuleTierDialog.dialog.id);
}

function displayEditSecondaryRuleTierDialog(tier, primaryTiers) {
    initSecondaryRuleTierDialog(
        "Edit Secondary Rule Tier",
        primaryTiers,
        tier.tier_rate
    );
    // Show the dialog
    showDialog(secondaryRuleTierDialog.dialog.id);
}

/*
 * Rule Display Helper Functions
 */
function displayFlatRateRule(rulesetRulesDisplay, ruleset, rule) {
    ruleDisplay = document.getElementById(flatRateRuleDisplay.card.id).cloneNode(true);
    ruleDisplay.classList.remove("hidden");
    ruleDisplay.id += "-" + ruleDisplay.id;
    
    ruleNameDisplay = ruleDisplay.querySelector("#" + flatRateRuleDisplay.name.id);
    ruleNameDisplay.id += "-" + rule.id;
    ruleNameDisplay.innerHTML = rule.name;

    ruleVariableNameDisplay = ruleDisplay.querySelector("#" + flatRateRuleDisplay.variableName.id);
    ruleVariableNameDisplay.id += "-" + rule.id;
    ruleVariableNameDisplay.innerHTML = rule.variable_name;

    ruleExplainerDisplay = ruleDisplay.querySelector("#" + flatRateRuleDisplay.explainer.id);
    if (rule.explainer == null || rule.explainer == "") {
        ruleExplainerDisplay.classList.add("hidden");
    }
    ruleExplainerDisplay.id += "-" + rule.id;
    ruleExplainerDisplay.innerHTML = rule.explainer;

    ruleTaxRateDisplay = ruleDisplay.querySelector("#" + flatRateRuleDisplay.taxRate.id);
    ruleTaxRateDisplay.id += "-" + rule.id;
    ruleTaxRateDisplay.innerHTML = rule.tax_rate;

    // Set event handlers on buttons
    ruleDisplay.querySelector(".edit-button").onclick = function() { editRule(ruleset, rule); }
    ruleDisplay.querySelector(".delete-button").onclick = function() { deleteRule(ruleset, rule); }
    ruleDisplay.querySelector(".move-up-button").onclick = function() { moveRuleUp(ruleset, rule); }
    ruleDisplay.querySelector(".move-down-button").onclick = function() { moveRuleDown(ruleset, rule); }
    
    rulesetRulesDisplay.appendChild(ruleDisplay);
}

function displayTieredRateRule(rulesetRulesDisplay, ruleset, rule) {
    ruleDisplay = document.getElementById(tieredRateRuleDisplay.card.id).cloneNode(true);
    ruleDisplay.classList.remove("hidden");
    ruleDisplay.id += "-" + ruleDisplay.id;
    
    ruleNameDisplay = ruleDisplay.querySelector("#" + tieredRateRuleDisplay.name.id);
    ruleNameDisplay.id += "-" + rule.id;
    ruleNameDisplay.innerHTML = rule.name;

    ruleVariableNameDisplay = ruleDisplay.querySelector("#" + tieredRateRuleDisplay.variableName.id);
    ruleVariableNameDisplay.id += "-" + rule.id;
    ruleVariableNameDisplay.innerHTML = rule.variable_name;

    ruleExplainerDisplay = ruleDisplay.querySelector("#" + tieredRateRuleDisplay.explainer.id);
    if (rule.explainer == null || rule.explainer == "") {
        ruleExplainerDisplay.classList.add("hidden");
    }
    ruleExplainerDisplay.id += "-" + rule.id;
    ruleExplainerDisplay.innerHTML = rule.explainer;

    // Set event handlers on buttons
    ruleDisplay.querySelector(".edit-button").onclick = function() { editRule(ruleset, rule); }
    ruleDisplay.querySelector(".delete-button").onclick = function() { deleteRule(ruleset, rule); }
    ruleDisplay.querySelector(".move-up-button").onclick = function() { moveRuleUp(ruleset, rule); }
    ruleDisplay.querySelector(".move-down-button").onclick = function() { moveRuleDown(ruleset, rule); }
    
    rulesetRulesDisplay.appendChild(ruleDisplay);
}

function displaySecondaryTieredRateRule(rulesetRulesDisplay, ruleset, rule) {
    ruleDisplay = document.getElementById(secondaryTieredRateRuleDisplay.card.id).cloneNode(true);
    ruleDisplay.classList.remove("hidden");
    ruleDisplay.id += "-" + ruleDisplay.id;
    
    ruleNameDisplay = ruleDisplay.querySelector("#" + secondaryTieredRateRuleDisplay.name.id);
    ruleNameDisplay.id += "-" + rule.id;
    ruleNameDisplay.innerHTML = rule.name;

    ruleVariableNameDisplay = ruleDisplay.querySelector("#" + secondaryTieredRateRuleDisplay.variableName.id);
    ruleVariableNameDisplay.id += "-" + rule.id;
    ruleVariableNameDisplay.innerHTML = rule.variable_name;

    ruleExplainerDisplay = ruleDisplay.querySelector("#" + secondaryTieredRateRuleDisplay.explainer.id);
    if (rule.explainer == null || rule.explainer == "") {
        ruleExplainerDisplay.classList.add("hidden");
    }
    ruleExplainerDisplay.id += "-" + rule.id;
    ruleExplainerDisplay.innerHTML = rule.explainer;

    ruleExplainerDisplay = ruleDisplay.querySelector("#" + secondaryTieredRateRuleDisplay.primaryRule.id);
    ruleExplainerDisplay.id += "-" + rule.id;
    ruleExplainerDisplay.innerHTML = rule.primary_rule.name;

    // Set event handlers on buttons
    ruleDisplay.querySelector(".edit-button").onclick = function() { editRule(ruleset, rule); }
    ruleDisplay.querySelector(".delete-button").onclick = function() { deleteRule(ruleset, rule); }
    ruleDisplay.querySelector(".move-up-button").onclick = function() { moveRuleUp(ruleset, rule); }
    ruleDisplay.querySelector(".move-down-button").onclick = function() { moveRuleDown(ruleset, rule); }
    
    rulesetRulesDisplay.appendChild(ruleDisplay);
}

function displayRuleset(ruleset) {
    display = document.getElementById(rulesetDisplay.card.id).cloneNode(true);
    display.classList.remove("hidden");
    display.id += "-" + ruleset.id;
    
    rulesetNameDisplay = display.querySelector("#" + rulesetDisplay.name.id);
    rulesetNameDisplay.id += "-" + ruleset.id;
    rulesetNameDisplay.innerHTML = ruleset.name;

    rulesetTaxCategoryDisplay = display.querySelector("#" + rulesetDisplay.taxCategpry.id);
    rulesetTaxCategoryDisplay.id += "-" + ruleset.id;
    rulesetTaxCategoryDisplay.innerHTML = getTaxCategoryById(ruleset.tax_category_id).name;

    rulesetRulesDisplay = display.querySelector("#" + rulesetDisplay.rules.id);
    rulesetRulesDisplay.id += "-" + ruleset.id;

    document.getElementById(rulesetsDisplayContainer.id).appendChild(display);

    // Set event handlers on buttons
    display.querySelector(".add-rule-button").onclick = function() { addRule(ruleset); }
    display.querySelector(".delete-ruleset-button").onclick = function() { deleteRuleset(ruleset); }
    display.querySelector(".move-ruleset-up-button").onclick = function() { moveRulesetUp(ruleset); }
    display.querySelector(".move-ruleset-down-button").onclick = function() { moveRulesetDown(ruleset); }

    // Display rules
    ruleset.rules.forEach(rule => {
        switch(rule.type) {
            case "flat_rate":
                    displayFlatRateRule(rulesetRulesDisplay, ruleset, rule);
                break;
            case "tiered_rate":
                    displayTieredRateRule(rulesetRulesDisplay, ruleset, rule);
                break;
            case "secondary_tiered_rate":
                    displaySecondaryTieredRateRule(rulesetRulesDisplay, ruleset, rule);
                break;
        }
    });
}

function updateRulesetsDisplay(rulesets) {
    resetContainer(rulesetsDisplayContainer.id, [rulesetDisplay.card.id]);

    rulesets.forEach(ruleset => {
        displayRuleset(ruleset);
    });
}

module.exports = {
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
};