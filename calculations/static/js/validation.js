function isBooleanFieldValid(id) {
    return $('input:radio[name="' + id + '"]:checked').length == 1;
}

function isFloatFieldValid(id) {
    let value = document.getElementById(id).value;
    return !isNaN(parseFloat(value)) && isFinite(value);
}

function isIntegerFieldValid(id) {
    let value = document.getElementById(id).value;
    return !isNaN(parseInt(value)) && isFinite(value);
}

function isSingleSelectFieldValid(id) {
    return $('input[name="' + id + '"]:checked').length == 1;
}

function showFormErrors(errors) {
    document.getElementById("errors").innerHTML = errors.join("");
}

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