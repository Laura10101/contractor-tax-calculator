/* jshint esversion: 8 */
if (typeof require !== "undefined") {
    const viewConsts = require("./view_consts.js");
    const viewModels = require("./view_models.js");
    require("bootstrap");
    $ = require("jquery");
    // View Constants
    dialogStates = viewConsts.dialogStates;
    endpoints = viewConsts.endpoints;
    statusDialog = viewConsts.statusDialog;
    confirmationDialog = viewConsts.confirmationDialog;
    jurisdictionsSelect = viewConsts.jurisdictionsSelect;
    questionTypeDialog = viewConsts.questionTypeDialog;
    booleanQuestionDialog = viewConsts.booleanQuestionDialog;
    numericQuestionDialog = viewConsts.numericQuestionDialog;
    multipleChoiceQuestionDialog = viewConsts.multipleChoiceQuestionDialog;
    multipleChoiceOptionDialog = viewConsts.multipleChoiceOptionDialog;
    questionDisplayContainer = viewConsts.questionDisplayContainer;
    booleanQuestionDisplay = viewConsts.booleanQuestionDisplay;
    numericQuestionDisplay = viewConsts.numericQuestionDisplay;
    multipleChoiceQuestionDisplay = viewConsts.multipleChoiceQuestionDisplay;
    rulesetDialog = viewConsts.rulesetDialog;
    ruleTypeDialog = viewConsts.ruleTypeDialog;
    flatRateRuleDialog = viewConsts.flatRateRuleDialog;
    tieredRateRuleDialog = viewConsts.tieredRateRuleDialog;
    secondaryTieredRateRuleDialog = viewConsts.secondaryTieredRateRuleDialog;
    ruleTierDialog = viewConsts.ruleTierDialog;
    secondaryRuleTierDialog = viewConsts.secondaryRuleTierDialog;
    rulesetsDisplayContainer = viewConsts.rulesetsDisplayContainer;
    rulesetDisplay = viewConsts.rulesetDisplay;
    flatRateRuleDisplay = viewConsts.flatRateRuleDisplay;
    tieredRateRuleDisplay = viewConsts.tieredRateRuleDisplay;
    secondaryTieredRateRuleDisplay = viewConsts.secondaryTieredRateRuleDisplay;

    // View models
    app = viewModels.app;
    getTaxCategoryById = viewModels.getTaxCategoryById;
    findPrimaryRuleTierById = viewModels.findPrimaryRuleTierById;
    taxCategoryHasRulesetForJurisdiction = viewModels.taxCategoryHasRulesetForJurisdiction;
    getValidQuestionTextVariableNamePairs = viewModels.getValidQuestionTextVariableNamePairs;
}
/*
 * Dialog Helper Functions
 */

// Display a general status message
function showMessage(message, title="An Error Occurred") {
    document.getElementById(statusDialog.label.id).innerHTML = title;
    document.getElementById(statusDialog.message.id).innerHTML = message;
    showDialog(statusDialog.dialog.id);
}

// Display an error message specifically
function error(message) {
    showMessage(message);
}

// Display a success message specifically
function success(message) {
    showMessage(message, "Success");
}

// Display a confirmation dialog box
function confirm(message, onConfirm) {
    document.getElementById(confirmationDialog.message.id).innerHTML = message;
    document.getElementById(confirmationDialog.confirmationButton.id).onclick = onConfirm;
    showDialog(confirmationDialog.dialog.id);
}

// Show a bootstrap modal with the given ID
function showDialog(dialogId) {
    $("#" + dialogId).modal("show");
}

// Hide a bootstrap modal with the given ID
function hideDialog(dialogId) {
    $("#" + dialogId).modal("hide");
}

/*
 * Validation Error Helper Functions
 */
function displayValidationErrors(errorContainerId, errors) {
    let errorContainer = document.getElementById(errorContainerId);
    errorContainer.innerHTML = errors.join("");
}

function clearValidationErrors(errorContainerId) {
    let errorContainer = document.getElementById(errorContainerId);
    errorContainer.innerHTML = "";
}

/*
 * DOM Helper Functions
 */

// Remove all child nodes of a parent DOM element
// Taken from https://www.javascripttutorial.net/dom/manipulating/remove-all-child-nodes/
function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

// Remove all children of a container except for the given list of prototype elements
function resetContainer(containerId, prototypeIds) {
    // Get the prototypes into an array
    prototypes = {};
    prototypeIds.forEach(prototypeId => {
        prototypes[prototypeId] = document.getElementById(prototypeId);
    });

    // Clear the container
    container = document.getElementById(containerId);
    removeAllChildNodes(container);

    // Add the prototypes back in
    for (const prototypeId in prototypes) {
        container.appendChild(prototypes[prototypeId]);
    }
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

/*
 * Jurisdiction Select Helper Functions
 */

// Display a list of jurisdictions in the jurisdictions select and set the onChange callback
function initJurisdictionsSelect(jurisdictions, selectionChangedCallback) {
    // Get the jurisdictions select box
    let select = document.getElementById(jurisdictionsSelect.id);

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

// Return the id of the selected jurisdiction
function getSelectedJurisdictionId() {
    return document.getElementById(jurisdictionsSelect.id).value;
}

/*
 * Validation Helpers
 */
function floatIsValid(value) {
    return !isNaN(parseFloat(value));
}

function intIsValid(value) {
    return !isNaN(parseInt(value));
}

/*
 * Question Dialog Helper Functions
 */
function validateQuestionData(text, variableName, questionId) {
    let errors = [];
    if (text == "" || text.length < 3) {
        errors.push("<p>The question text is a required field and its length must be > 3 characters</p>");
    }

    // If the question has no ID or the variable name has changed
    // Validate the variable name
    if (questionId == null) {
        if (isDuplicateVariableName(variableName)) {
            errors.push("<p>A question already exists with the data name '" + variableName + "'. Data name must be unique<p>");
        }
    } else if (findQuestionById(questionId).variable_name != variableName) {
        if (isDuplicateVariableName(variableName)) {
            errors.push("<p>A question already exists with the data name '" + variableName + "'. Data name must be unique<p>");
        }
    }

    let varNameRegEx = RegExp("^[A-Za-z0-9-_]+$");
    if (!varNameRegEx.test(variableName)) {
        errors.push("<p>The variable name must contain only alphanumeric characters, hyphens or underscores.</p>");
    }

    return errors;
}

/*
 * Question Dialog Helper Functions - Boolean
 */

// Set the label and input values on a boolean question dialog
function initBooleanQuestionDialog(dialogLabel, questionText, explainer, variableName, isMandatory, canEditVariableName=true) {
    clearValidationErrors(booleanQuestionDialog.errors.id);
    document.getElementById(booleanQuestionDialog.label.id).innerText = dialogLabel;
    document.getElementById(booleanQuestionDialog.questionText.input.id).value = questionText;
    document.getElementById(booleanQuestionDialog.explainer.input.id).value = explainer;
    document.getElementById(booleanQuestionDialog.variableName.input.id).value = variableName;
    document.getElementById(booleanQuestionDialog.isMandatory.input.id).checked = isMandatory;

    document.getElementById(booleanQuestionDialog.variableName.input.id).readOnly = !canEditVariableName;
}

// Set up and display a create question dialog
function displayCreateBooleanQuestionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initBooleanQuestionDialog("Create Boolean Question", "", "", "", false);
    // Show the dialog
    showDialog(booleanQuestionDialog.dialog.id);
}

// Display the boolean question dialog box in edit mode
function displayEditBooleanQuestionDialog(question) {
    // Initialise the boolean question dialog with appropriate values for a create
    initBooleanQuestionDialog(
        "Edit Boolean Question",
        question.text,
        question.explainer,
        question.variable_name,
        question.is_mandatory,
        false
    );
    // Show the dialog
    showDialog(booleanQuestionDialog.dialog.id);
}

// Check if the current input in the boolean question dialog is valid
// If not, return a list of errors
function validateBooleanQuestionDialog(questionId=null) {
    let text = document.getElementById(booleanQuestionDialog.questionText.input.id).value;
    let variableName = document.getElementById(booleanQuestionDialog.variableName.input.id).value;
    let errors = validateQuestionData(text, variableName, questionId);
    return errors;
}


/*
 * Question Dialog Helper Functions - Numeric
 */
function initNumericQuestionDialog(dialogLabel, questionText, explainer, variableName, isMandatory, isInteger, minValue, maxValue, canEditVariableName=true) {
    clearValidationErrors(numericQuestionDialog.errors.id);
    document.getElementById(numericQuestionDialog.label.id).innerText = dialogLabel;
    document.getElementById(numericQuestionDialog.questionText.input.id).value = questionText;
    document.getElementById(numericQuestionDialog.explainer.input.id).value = explainer;
    document.getElementById(numericQuestionDialog.variableName.input.id).value = variableName;
    document.getElementById(numericQuestionDialog.isMandatory.input.id).checked = isMandatory;
    document.getElementById(numericQuestionDialog.isInteger.input.id).checked = isInteger;
    document.getElementById(numericQuestionDialog.minimumValue.input.id).value = minValue;
    document.getElementById(numericQuestionDialog.maximumValue.input.id).value = maxValue;

    document.getElementById(numericQuestionDialog.variableName.input.id).readOnly = !canEditVariableName;
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
        question.max_value,
        false
    );
    // Show the dialog
    showDialog(numericQuestionDialog.dialog.id);
}

// Check if the current input in the numeric question dialog is valid
// If not, return a list of errors
function validateNumericQuestionDialog(questionId=null) {
    let text = document.getElementById(numericQuestionDialog.questionText.input.id).value;
    let variableName = document.getElementById(numericQuestionDialog.variableName.input.id).value;
    let minValue = document.getElementById(numericQuestionDialog.minimumValue.input.id).value;
    let maxValue = document.getElementById(numericQuestionDialog.maximumValue.input.id).value;
    let errors = validateQuestionData(text, variableName, questionId);

    if (!intIsValid(minValue)) {
        errors.push("<p>Minimium value must be a valid integer (whole number)<p>");
    }

    if (!intIsValid(maxValue) && maxValue != "") {
        errors.push("<p>Maximum value must be a valid integer (whole number)</p>");
    }

    return errors;
}

/*
 * Question Dialog Helper Functions - Multiple Choice
 */
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

// Initialise the multiple choice question dialog
function initMultipleChoiceQuestionDialog(dialogLabel, questionText, explainer, variableName, isMandatory,
    allowMultiselect, options, showOptions=true, canEditVariableName=true) {
    clearValidationErrors(multipleChoiceQuestionDialog.errors.id);
    document.getElementById(multipleChoiceQuestionDialog.label.id).innerText = dialogLabel;
    document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value = questionText;
    document.getElementById(multipleChoiceQuestionDialog.explainer.input.id).value = explainer;
    document.getElementById(multipleChoiceQuestionDialog.variableName.input.id).value = variableName;
    document.getElementById(multipleChoiceQuestionDialog.isMandatory.input.id).checked = isMandatory;
    document.getElementById(multipleChoiceQuestionDialog.allowMultiselect.input.id).checked = allowMultiselect;
    let optionsRow = document.getElementById("options-row");
    if (showOptions) {
        if (optionsRow.classList.contains("hidden")) {
            optionsRow.classList.remove("hidden");
        }
    } else {
        if (!optionsRow.classList.contains("hidden")) {
            optionsRow.classList.add("hidden");
        }
    }
    // Update the options display
    updateMultipleChoiceQuestionDialogOptionsDisplay(options);

    document.getElementById(multipleChoiceQuestionDialog.variableName.input.id).readOnly = !canEditVariableName;
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
        question.options,
        true,
        false
    );
    // Show the dialog
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

function validateMultipleChoiceQuestionDialog(questionId=null) {
    let text = document.getElementById(multipleChoiceQuestionDialog.questionText.input.id).value;
    let variableName = document.getElementById(multipleChoiceQuestionDialog.variableName.input.id).value;
    let errors = validateQuestionData(text, variableName, questionId);
    return errors;
}

/*
 * Multiple Choice Option Helper Functions
 */
function initMultipleChoiceOptionDialog(name, explainer) {
    clearValidationErrors(multipleChoiceOptionDialog.errors.id);
    document.getElementById(multipleChoiceOptionDialog.name.input.id).value = name;
    document.getElementById(multipleChoiceOptionDialog.explainer.input.id).value = explainer;
}

function displayCreateMultipleChoiceOptionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initMultipleChoiceOptionDialog("", "");
    // Show the dialog
    showDialog(multipleChoiceOptionDialog.dialog.id);
}

function validateMultipleChoiceOptionDialog() {
    let errors = [];
    let name = document.getElementById(multipleChoiceOptionDialog.name.input.id).value;
    if (name == "" || name.length < 3) {
        errors.push("<p>Name is a required field and must be at least 3 characters</p>");
    }
    return errors;
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
 * Ruleset Dialog Helper Functions
 */

// Ruleset Dialog Helpers
function initRulesetDialog(dialogLabel, taxCategories) {
    clearValidationErrors(rulesetDialog.errors.id);
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
    initRulesetDialog("Create Tax Rule Collection", app.taxCategories);
    // Show the dialog
    showDialog(rulesetDialog.dialog.id);
}

// Check if the current input in the ruleset dialog is valid
// If not, return a list of errors
function validateRulesetDialog() {
    let taxCategoryId = document.getElementById(rulesetDialog.taxCategory.input.id).value;
    let errors = [];

    if (taxCategoryHasRulesetForJurisdiction(taxCategoryId)) {
        errors.push("<p>A ruleset already exists for this tax category. Please choose another tax category.</p>");
    }

    return errors;
}

/*
 * Rule Dialog Helper Functions - Rule Type
 */
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

/*
 * Rule Dialog Helper Functions - General Validation
 */
function validateRuleData(name) {
    let errors = [];
    if (name == "" || name.length < 3) {
        errors.push("<p>Name is a required field and must be at least 3 characters long</p>");
    }
    return errors;
}

function initVariableNamesSelect(selectId) {
    let select = document.getElementById(selectId);
    removeAllChildNodes(select);

    let variables = getValidQuestionTextVariableNamePairs();
    variables.forEach(variable => {
        option = document.createElement("option");
        option.text = variable.questionText + " (" + variable.variableName + ")";
        option.value = variable.variableName;
        select.add(option);
    });
}

/*
 * Rule Dialog Helper Functions - Flat Rate Rules
 */
// Flat Rate Rule Dialog Helpers
function initFlatRateRuleDialog(dialogLabel, name, explainer, variableName, taxRate) {
    clearValidationErrors(flatRateRuleDialog.errors.id);
    document.getElementById(flatRateRuleDialog.label.id).innerText = dialogLabel;
    document.getElementById(flatRateRuleDialog.name.input.id).value = name;
    document.getElementById(flatRateRuleDialog.explainer.input.id).value = explainer;
    initVariableNamesSelect(flatRateRuleDialog.variableName.input.id);
    document.getElementById(flatRateRuleDialog.variableName.input.id).value = variableName;
    document.getElementById(flatRateRuleDialog.taxRate.input.id).value = taxRate;
}

function displayCreateFlatRateRuleDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initFlatRateRuleDialog("Create Flat Rate", "", "", "", "");
    // Show the dialog
    showDialog(flatRateRuleDialog.dialog.id);
}

function displayEditFlatRateRuleDialog(rule) {
    initFlatRateRuleDialog(
        "Edit Flat Rate",
        rule.name,
        rule.explainer,
        rule.variable_name,
        rule.tax_rate
    );
    // Show the dialog
    showDialog(flatRateRuleDialog.dialog.id);
}

// Check if the current input in the rule dialog is valid
// If not, return a list of errors
function validateFlatRateRuleDialog() {
    let errors = [];

    let name = document.getElementById(flatRateRuleDialog.name.input.id).value;
    let taxRate = document.getElementById(flatRateRuleDialog.taxRate.input.id).value;

    errors = validateRuleData(name);

    if (!floatIsValid(taxRate)) {
        errors.push("<p>Tax rate is a required to be a valid decimal number</p>");
    }

    return errors;
}

/*
 * Rule Dialog Helper Functions - Tiered Rate Rules
 */
// Tiered Rate Rule Dialog Helpers
function initTieredRateRuleDialog(dialogLabel, name, explainer, variableName, tiers, showTiers=false) {
    clearValidationErrors(tieredRateRuleDialog.errors.id);
    document.getElementById(tieredRateRuleDialog.label.id).innerText = dialogLabel;
    document.getElementById(tieredRateRuleDialog.name.input.id).value = name;
    document.getElementById(tieredRateRuleDialog.explainer.input.id).value = explainer;
    initVariableNamesSelect(tieredRateRuleDialog.variableName.input.id);
    document.getElementById(tieredRateRuleDialog.variableName.input.id).value = variableName;
    let tiersRow = document.getElementById("tiers-row");
    if (showTiers) {
        if (tiersRow.classList.contains("hidden")) {
            tiersRow.classList.remove("hidden");
        }
    } else {
        if (!tiersRow.classList.contains("hidden")) {
            tiersRow.classList.add("hidden");
        }
    }
    updateRuleTierTable(true, tiers);
}

function displayCreateTieredRateRuleDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initTieredRateRuleDialog("Create Tiered Rate", "", "", "", [], false);
    // Show the dialog
    showDialog(tieredRateRuleDialog.dialog.id);
}

function displayEditTieredRateRuleDialog(rule) {
    initTieredRateRuleDialog(
        "Edit Tiered Rate",
        rule.name,
        rule.explainer,
        rule.variable_name,
        rule.tiers,
        true
    );
    // Show the dialog
    showDialog(tieredRateRuleDialog.dialog.id);
}

// Check if the current input in the rule dialog is valid
// If not, return a list of errors
function validateTieredRateRuleDialog() {
    let errors = [];

    let name = document.getElementById(tieredRateRuleDialog.name.input.id).value;

    errors = validateRuleData(name);

    return errors;
}

/*
 * Rule Dialog Helper Functions - Secondary Tiered Rate Rules
 */

// Secondary Tiered Rate Rule Dialog Helpers
function initPrimaryRulesSelect(rules) {
    let select = document.getElementById(secondaryTieredRateRuleDialog.primaryRule.input.id);
    removeAllChildNodes(select);

    rules.forEach(rule => {
        option = document.createElement("option");
        option.text = rule.name;
        option.value = rule.id;
        select.add(option);
    });
}

function initSecondaryTieredRateRuleDialog(dialogLabel, name, explainer, variableName, primaryRules, tiers, showTiers=true) {
    clearValidationErrors(secondaryTieredRateRuleDialog.errors.id);
    document.getElementById(secondaryTieredRateRuleDialog.label.id).innerText = dialogLabel;
    document.getElementById(secondaryTieredRateRuleDialog.name.input.id).value = name;
    document.getElementById(secondaryTieredRateRuleDialog.explainer.input.id).value = explainer;
    initVariableNamesSelect(secondaryTieredRateRuleDialog.variableName.input.id);
    document.getElementById(secondaryTieredRateRuleDialog.variableName.input.id).value = variableName;
    let tiersRow = document.getElementById("secondary-tiers-row");
    if (showTiers) {
        if (tiersRow.classList.contains("hidden")) {
            tiersRow.classList.remove("hidden");
        }
    } else {
        if (!tiersRow.classList.contains("hidden")) {
            tiersRow.classList.add("hidden");
        }
    }
    initPrimaryRulesSelect(primaryRules);
    updateRuleTierTable(false, tiers);
}

function displayCreateSecondaryTieredRateRuleDialog(primaryRules) {
    // Initialise the boolean question dialog with appropriate values for a create
    initSecondaryTieredRateRuleDialog("Create Progressive Tiered Rate", "", "", "", primaryRules, [], false);
    // Show the dialog
    showDialog(secondaryTieredRateRuleDialog.dialog.id);
}

function displayEditSecondaryTieredRateRuleDialog(rule, primaryRules) {
    initSecondaryTieredRateRuleDialog(
        "Edit Progressive Tiered Rate",
        rule.name,
        rule.explainer,
        rule.variable_name,
        primaryRules,
        rule.tiers,
        true
    );
    // Show the dialog
    showDialog(secondaryTieredRateRuleDialog.dialog.id);
}

// Check if the current input in the rule dialog is valid
// If not, return a list of errors
function validateSecondaryTieredRateRuleDialog() {
    let errors = [];

    let name = document.getElementById(secondaryTieredRateRuleDialog.name.input.id).value;

    errors = validateRuleData(name);
    
    return errors;
}

/*
 * Rule Tier Dialog Helper Functions
 */

// Primary Rule Tier Dialog Helpers
function initRuleTierDialog(dialogLabel, minValue, maxValue, taxRate) {
    clearValidationErrors(ruleTierDialog.errors.id);
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

// Check if the current input in the rule tier dialog is valid
// If not, return a list of errors
function validateRuleTierDialog() {
    let errors = [];

    let minValue = document.getElementById(ruleTierDialog.minimumValue.input.id).value;
    let maxValue = document.getElementById(ruleTierDialog.maximumValue.input.id).value;
    let taxRate = document.getElementById(ruleTierDialog.taxRate.input.id).value;

    if (!intIsValid(minValue)) {
        errors.push("<p>Minimum value is required to be a valid integer</p>");
    }

    if (!intIsValid(maxValue) && maxValue != "") {
        errors.push("<p>Maximum value is required to be a valid integer</p>");
    }

    if (!floatIsValid(taxRate)) {
        errors.push("<p>Tax rate is required to be a valid decimal number</p>");
    }
    
    return errors;
}

/*
 * Secondary Rule Tier Dialog Helper Functions
 */
// Secondary Rule Tier Dialog Helpers
function initPrimaryRuleTiersSelect(tiers) {
    let select = document.getElementById(secondaryRuleTierDialog.primaryTier.input.id);
    removeAllChildNodes(select);
    
    tiers.forEach(tier => {
        option = document.createElement("option");
        option.text = tier.min_value + " - " + tier.max_value + " (" + tier.tier_rate + ")";
        option.value = tier.id;
        select.add(option);
    });
}

function initSecondaryRuleTierDialog(dialogLabel, primaryRuleTiers, taxRate) {
    clearValidationErrors(secondaryRuleTierDialog.errors.id);
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

// Check if the current input in the rule tier dialog is valid
// If not, return a list of errors
function validateSecondaryRuleTierDialog() {
    let errors = [];

    let taxRate = document.getElementById(secondaryRuleTierDialog.taxRate.input.id).value;

    if (!floatIsValid(taxRate)) {
        errors.push("<p>Tax rate is required to be a valid decimal number</p>");
    }
    
    return errors;
}

/*
 * Rule Display Helper Functions
 */
function displayFlatRateRule(rulesetRulesDisplay, ruleset, rule) {
    ruleDisplay = document.getElementById(flatRateRuleDisplay.card.id).cloneNode(true);
    ruleDisplay.classList.remove("hidden");
    ruleDisplay.id += "-" + rule.id;
    
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
    ruleDisplay.id += "-" + rule.id;
    
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
    ruleDisplay.id += "-" + rule.id;
    
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

    primaryRuleDisplay = ruleDisplay.querySelector("#" + secondaryTieredRateRuleDisplay.primaryRule.id);
    primaryRuleDisplay.id += "-" + rule.id;
    primaryRuleDisplay.innerHTML = rule.primary_rule.name;

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

if (typeof module !== "undefined") module.exports = {
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
    updateRulesetsDisplay,
    initBooleanQuestionDialog,
    initNumericQuestionDialog,
    initMultipleChoiceQuestionDialog,
    initMultipleChoiceOptionDialog,
    initRulesetDialog,
    initFlatRateRuleDialog,
    initTieredRateRuleDialog,
    initSecondaryTieredRateRuleDialog,
    initRuleTierDialog,
    initSecondaryRuleTierDialog,
    validateBooleanQuestionDialog,
    validateNumericQuestionDialog,
    validateMultipleChoiceQuestionDialog,
    validateMultipleChoiceOptionDialog,
    validateRulesetDialog,
    validateRuleData,
    validateFlatRateRuleDialog,
    validateTieredRateRuleDialog,
    validateSecondaryTieredRateRuleDialog,
    validateRuleTierDialog,
    validateSecondaryRuleTierDialog,
    displayValidationErrors
};