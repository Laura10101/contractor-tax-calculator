
// A booelan field is valid if exactly one response has been checked
function isBooleanFieldValid(id) {
    return $('input:radio[name="' + id + '"]:checked').length == 1;
}

// A float field is valid only if a valid integer or floating point nunmber has been entered
function isFloatFieldValid(id) {
    let value = document.getElementById(id).value;
    return !isNaN(parseFloat(value)) && isFinite(value);
}


// An integer is valid only if a valid integer has been entered
function isIntegerFieldValid(id) {
    let value = document.getElementById(id).value;
    return !isNaN(parseInt(value)) && isFinite(value);
}

// A single select is valid if exactly one box has been checked
function isSingleSelectFieldValid(id) {
    return $('input[name="' + id + '"]:checked').length == 1;
}

// Concatenate all errors and display in the error box
function showFormErrors(errors) {
    document.getElementById("errors").innerHTML = errors.join("");
}

// Get the label corresponding to the given field
function getLabelValue(id) {
    return document.getElementById(id + "-title").innerHTML;
}


// Deduplicate an array
// Taken from: https://builtin.com/software-engineering-perspectives/remove-duplicates-from-array-javascript
function deduplicate(arr) {
    let unique = [];
    arr.forEach(val => {
        if (!unique.includes(val)) {
            unique.push(val);
        }
    });
    return unique;
}

// Iterate through each field and validate it, adding the
// errors if a field is not valid. Submit the form only if all fields are valid
function validateForm() {
    let errors = [];

    $("input").each(function(i, el) {
        if (el.classList.contains("boolean")) {
            if (!isBooleanFieldValid(el.name)) {
                errors.push('<p>Field "' + getLabelValue(el.name) + '" is required. Please select either Yes or No.</p>');
            }
        } else if (el.classList.contains("float")) {
            if (!isFloatFieldValid(el.id)) {
                errors.push('<p>Field "' + getLabelValue(el.name) + '" is required to be numeric. Please enter a valid number. Decimals are valid.</p>');
            }
        } else if (el.classList.contains("integer")) {
            if (!isIntegerFieldValid(el.id)) {
                errors.push('<p>Field "' + getLabelValue(el.name) + '" is required to be numeric. Please enter a valid number. Decimals are <b>not</b> valid.</p>');
            }
        } else if (el.classList.contains("single-select")) {
            if (!isSingleSelectFieldValid(el.name)) {
                errors.push('<p>Field "' + getLabelValue(el.name) + '" requires exactly one value to be selected.</p>');
            }
        }
    });

    showFormErrors(deduplicate(errors));

    if (errors == "") {
        document.getElementById("jurisdiction-forms").submit();
    }
}