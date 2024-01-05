/*
 * General Helper Functions
 */

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

/*
 * Question Dialog Helper Functions
 */

// Handle selection of a question type via question type modal
function questionTypeChosen() {
    // Close the modal
    hideDialog(questionTypeDialog.dialog.id);

    // Display the appropraite create question dialog for the selected question type
    questionType = document.getElementById(questionTypeDialog.questionType.input.id).value;
    switch(questionType) {
        case "boolean":
            displayCreateBooleanQuestionDialog();
        break;

        case "numeric":
            displayCreateNumericQuestionDialog();
        break;
        
        case "multiple_choice":
            displayCreateMultipleChoiceQuestionDialog();
        break;
    }
}

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
        question.variableName,
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
    initBooleanQuestionDialog("Create Numeric Question", "", "", "", false, false, "", "");
    // Show the dialog
    showDialog(numericQuestionDialog.dialog.id);
}

function displayEditNumericQuestionDialog(question) {
    initNumericQuestionDialog(
        "Edit Numeric Question",
        question.text,
        question.explainer,
        question.variableName,
        question.is_mandatory,
        question.is_integer,
        question.min_value,
        question.max_value
    );
}

// Multiple Choice Question Dialog
function updateMultipleChoiceQuestionDialogOptionsDisplay(options) {

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
    initBooleanQuestionDialog("Create Multiple Choice Question", "", "", "", false, false, []);
    // Show the dialog
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

function displayEditMultipleChoiceQuestionDialog() {
    // Initialise the boolean question dialog with appropriate values for a create
    initBooleanQuestionDialog(
        "Edit Multiple Choice Question",
        question.text,
        question.explainer,
        question.variableName,
        question.is_mandatory,
        question.is_multiselect,
        question.options
    );
    // Show the dialog
    showDialog(multipleChoiceQuestionDialog.dialog.id);
}

/*
 * Question Display Helper Functions
 */

/*
 * Rule Dialog Helper Functions
 */

/*
 * Rule Display Helper Functions
 */