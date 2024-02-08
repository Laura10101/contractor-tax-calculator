/* jshint esversion: 8 */
/*
 * service_clients.js
 * Provides wrapper functions for easy access to required API endpoints
 */
if (typeof require !== "undefined") {
    $ = require("jquery");
    const viewConsts = require("./view_consts.js");
    const viewModels = require("./view_models.js");
    endpoints = viewConsts.endpoints;
    app = viewModels.app;
}

/*
 * Helper functions for HTTP requests
 */
function getCSRFCookie() {
    let name = "csrftoken";
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Generate a querystring from a JSON object
function queryToString(query) {
    let queryString = "";
    for (const key in query) {
        if (query.hasOwnProperty(key)) {
            if (queryString == "") {
                queryString = key + "=" + query[key];   
            } else {
                queryString += "&" + key + "=" + query[key];
            }
        }
    }
    return queryString;
}

// Generate an absolute URL from a relative URL
function toUrl(endpoint) {
    return app.apiHost.protocol + "//" + app.apiHost.hostname + "/api/" + endpoint;
}

// Perform an asynchronous update on all elements in a queue
// and then call a given function once all elements have been processed
function processBatch(requestQueue, updater, onQueueEmpty) {
    if (requestQueue.length > 0) {
        console.log("Process batch");
        let batchSize = 3;
        let batch = [];
        for (var i = 0; i < batchSize; i++) {
            if (requestQueue.length > 0) {
                let item = requestQueue.pop();
                batch.push(updater(item));
            }
        }
        $.when(...batch).then(function() { processBatch(requestQueue, updater, onQueueEmpty); });
    } else {
        onQueueEmpty();
    }
}

// Retrieve data from an API by invoking an HTTP GET request
// on an API endpoint with a query string added
function query(endpoint, query, success, error) {
    let url = toUrl(endpoint);
    return $.ajax({
        type: "GET",
        url: query == null ? url: url + "?" + queryToString(query),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

// Retrieve data from an API by invoking an HTTP GET request
// on an API endpoint without a query string added
function get(endpoint, id, success, error) {
    let url = toUrl(endpoint);
    return $.ajax({
        type: "GET",
        url: url + id + "/",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

// Create a new entity via an API by triggering an
// HTTP POST request
function post(endpoint, data, success, error) {
    let url = toUrl(endpoint);
    return $.ajax({
        type: "POST",
        url: url,
        headers: { 'X-CSRFToken': getCSRFCookie() },
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

// Update an entity via an API by triggering an HTTP PUT
// request
function put(endpoint, id, data, success, error) {
    let url = toUrl(endpoint);
    return $.ajax({
        type: "PUT",
        url: url + id + "/",
        headers: { 'X-CSRFToken': getCSRFCookie() },
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

// Update an entity via an API by triggering an HTTP PATCH
// request
function patch(endpoint, id, data, success, error) {
    let url = toUrl(endpoint);
    return $.ajax({
        type: "PATCH",
        url: url + id + "/",
        headers: { 'X-CSRFToken': getCSRFCookie() },
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

// Delete an entity via an API by triggering an HTTP DELETE
// request
function remove(endpoint, id, success, error) {
    let url = toUrl(endpoint);
    return $.ajax({
        type: "DELETE",
        url: url + id + "/",
        headers: { 'X-CSRFToken': getCSRFCookie() },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

/*
 * Jurisdictions service client
 */

// Get all jurisdictions data via the jurisdiction API
function getJurisdictions(onSuccess, onFailure) {
    return query(endpoints.jurisdictions.base, null, onSuccess, onFailure);
}

/*
 * Tax categories service client
 */

// Get all tax category data via the rules API
function getTaxCategories(onSuccess, onFailure) {
    return query(endpoints.rules.taxCategories, null, onSuccess, onFailure);
}

/*
 * Forms service client
 */

// Get all form and question data for a given jurisdiction via the forms API
function getFormForJurisdiction(jurisdictionId, onSuccess, onFailure) {
    let queryParameters = {
        jurisdiction_ids: jurisdictionId
    };
    return query(endpoints.forms.base, queryParameters, onSuccess, onFailure);
}

/*
 * Questions service client
 */

// Create a new boolean question entity via the forms API based on the given data
function createBooleanQuestion(formId, text, ordinal, explainer, variableName, isMandatory, onSuccess, onFailure) {
    let data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        variable_name: variableName,
        is_mandatory: isMandatory,
        type: "boolean"
    };
    return post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

// Update an existing boolean question entity via the forms API based on the given data
function updateBooleanQuestion(formId, questionId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    let data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "boolean"
    };
    return put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

// Create a new numeric question entity via the forms API based on the given data
function createNumericQuestion(formId, text, ordinal, explainer, variableName, isMandatory, isInteger, minValue, maxValue, onSuccess, onFailure) {
    let data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        variable_name: variableName,
        is_mandatory: isMandatory,
        type: "numeric",
        is_integer: isInteger,
        min_value: !isNaN(parseInt(minValue)) ? parseInt(minValue) : null,
        max_value: !isNaN(parseInt(maxValue)) ? parseInt(maxValue) : null
    };
    return post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

// Update an existing numeric question entity via the forms API based on the given data
function updateNumericQuestion(formId, questionId, text, ordinal, explainer, isMandatory, isInteger, minValue, maxValue, onSuccess, onFailure) {
    let data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "numeric",
        is_integer: isInteger,
        min_value: !isNaN(parseInt(minValue)) ? parseInt(minValue) : null,
        max_value: !isNaN(parseInt(maxValue)) ? parseInt(maxValue) : null
    };
    return put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

// Create a new multiple choice question entity via the forms API based on the given data
function createMultipleChoiceQuestion(formId, text, ordinal, explainer, variableName, isMandatory, onSuccess, onFailure) {
    let data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        variable_name: variableName,
        is_mandatory: isMandatory,
        type: "multiple_choice"
    };
    return post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

// Update an existing multiple choice question entity via the forms API based on the given data
function updateMultipleChoiceQuestion(formId, questionId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    let data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "multiple_choice"
    };
    return put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

// Helper function to update a question entity via the forms API
// based on the provided question object
// Invoke the appropriate API call based on the type of the given question object
function updateQuestion(question, onSuccess, onFailure) {
    let formId = getFormId();
    switch (question.type) {
        case "boolean":
                return updateBooleanQuestion(formId, question.id, question.text, question.ordinal, question.explainer, question.is_mandatory, onSuccess, onFailure);
        case "numeric":
                return updateNumericQuestion(
                    formId,
                    question.id,
                    question.text,
                    question.ordinal,
                    question.explainer,
                    question.is_mandatory,
                    question.is_integer,
                    question.min_value,
                    question.max_value,
                    onSuccess,
                    onFailure);
        case "multiple_choice":
                return updateMultipleChoiceQuestion(formId, question.id, question.text, question.ordinal, question.explainer, question.is_mandatory, onSuccess, onFailure);
    }
}

// Remove a question entity via the forms API based on the given question ID
function removeQuestion(formId, questionId, onSuccess, onFailure) {
    return remove(endpoints.forms.questions(formId), questionId, onSuccess, onFailure);
}

/*
 * Multiple choice options service client
 */

// Create a new multiple choice option entity via the forms API based on the given data
function postMultipleChoiceOption(formId, questionId, text, explainer, onSuccess, onFailure) {
    let data = {
        text: text,
        explainer: explainer
    };
    return post(endpoints.forms.multipleChoiceOptions(formId, questionId), data, onSuccess, onFailure);
}

// Remove a multiple choice option entity via the forms API based on the given option ID
function removeMultipleChoiceOption(formId, questionId, optionId, onSuccess, onFailure) {
    return remove(endpoints.forms.multipleChoiceOptions(formId, questionId), optionId, onSuccess, onFailure);
}

/*
 * Rulesets service client
 */

// Retrieve all rulesets and rules for a given jurisdiction
function getRulesetsForJurisdiction(jurisdictionId, onSuccess, onFailure) {
    let queryParameters = {
        jurisdiction_id: jurisdictionId
    };
    return query(endpoints.rules.rulesets, queryParameters, onSuccess, onFailure);
}

// Create a new ruleset entity via the rules API based on the given data
function postRuleset(jurisdictionId, taxCategoryId, ordinal, onSuccess, onFailure) {
    let data = {
        jurisdiction_id: parseInt(jurisdictionId),
        tax_category_id: parseInt(taxCategoryId),
        ordinal: ordinal
    };
    return post(endpoints.rules.rulesets, data, onSuccess, onFailure);
}

// Update an existing ruleset entity via the rules API based on the given data
function patchRuleset(rulesetId, ordinal, onSuccess, onFailure) {
    let data = {
        ordinal: ordinal
    };
    return patch(endpoints.rules.rulesets, rulesetId, data, onSuccess, onFailure);
}

// Remove a ruleset entity via the rules API based on the given data
function removeRuleset(rulesetId, onSuccess, onFailure) {
    return remove(endpoints.rules.rulesets, rulesetId, onSuccess, onFailure);
}

/*
 * Rules service client
 */

// Create a new flat rate rule entity via the rules API based on the given data
function createFlatRateRule(rulesetId, name, explainer, variableName, ordinal, taxRate, onSuccess, onFailure) {
    let data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "flat_rate",
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

// Update an existing flat rate rule entity via the rules API based on the given data
function updateFlatRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, taxRate, onSuccess, onFailure) {
    let data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "flat_rate",
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

// Create a new tiered rate rule entity via the rules API based on the given data
function createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, onSuccess, onFailure) {
    let data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "tiered_rate"
    };
    return post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

// Update an existing tiered rate rule entity via the rules API based on the given data
function updateTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, onSuccess, onFailure) {
    let data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "tiered_rate"
    };
    return put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

// Create a new secondary tiered rate rule entity via the rules API based on the given data
function createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, primaryRuleId, onSuccess, onFailure) {
    let data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "secondary_tiered_rate",
        primary_rule_id: parseInt(primaryRuleId)
    };
    return post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

// Update an existing secondary tiered rate rule entity via the rules API based on the given data
function updateSecondaryTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, primaryRuleId, onSuccess, onFailure) {
    let data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "secondary_tiered_rate",
        primary_rule_id: parseInt(primaryRuleId)
    };
    return put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

// Helper function to update a rule via the rules API based on the given rule object
// Call the appropriate updater via based on the type of the given rule
function updateRule(rulesetId, rule, flatRateRuleUpdater, tieredRateRuleUpdater, secondaryTieredRateRuleUpdater, onSuccess, onFailure) {
    switch (rule.type) {
        case "flat_rate":
                flatRateRuleUpdater(
                    rulesetId,
                    rule.id,
                    rule.name,
                    rule.explainer,
                    rule.variable_name,
                    rule.ordinal,
                    rule.tax_rate,
                    onSuccess,
                    onFailure
                );
            break;
        case "tiered_rate":
                tieredRateRuleUpdater(
                    rulesetId,
                    rule.id,
                    rule.name,
                    rule.explainer,
                    rule.variable_name,
                    rule.ordinal,
                    onSuccess,
                    onFailure
                );
            break;
        case "secondary_tiered_rate":
                secondaryTieredRateRuleUpdater(
                    rulesetId,
                    rule.id,
                    rule.name,
                    rule.explainer,
                    rule.variable_name,
                    rule.ordinal,
                    rule.primary_rule.id,
                    onSuccess,
                    onFailure
                );
            break;
    }
}

// Remove an existing rule entity via the rules API based on the given data
function removeRule(rulesetId, ruleId, onSuccess, onFailure) {
    return remove(endpoints.rules.rules(rulesetId), ruleId, onSuccess, onFailure);
}

/*
 * Rule tiers service client
 */

// Create a new rule tier entity via the rules API based on the given data
function postRuleTier(rulesetId, ruleId, minValue, maxValue, ordinal, taxRate, onSuccess, onFailure) {
    let data = {
        min_value: !isNaN(parseInt(minValue)) ? parseInt(minValue) : null,
        max_value: !isNaN(parseInt(maxValue)) ? parseInt(maxValue) : null,
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return post(endpoints.rules.tiers(rulesetId, ruleId), data, onSuccess, onFailure);
}

// Update an existing rule tier entity via the rules API based on the given data
function updateRuleTier(rulesetId, ruleId, tierId, minValue, maxValue, ordinal, taxRate, onSuccess, onFailure) {
    let data = {
        min_value: !isNaN(parseInt(minValue)) ? parseInt(minValue) : null,
        max_value: !isNaN(parseInt(maxValue)) ? parseInt(maxValue) : null,
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return put(endpoints.rules.tiers(rulesetId, ruleId), tierId, data, onSuccess, onFailure);
}

// Remove an existing rule tier entity via the rules API based on the given rule tier ID
function removeRuleTier(rulesetId, ruleId, tierId, onSuccess, onFailure) {
    return remove(endpoints.rules.tiers(rulesetId, ruleId), tierId, onSuccess, onFailure);
}

/*
 * Secondary rule tiers service client
 */

// Create a new secondary rule tier entity via the rules API based on the given data
function postSecondaryRuleTier(rulesetId, ruleId, primaryTierId, ordinal, taxRate, onSuccess, onFailure) {
    let data = {
        primary_tier_id: parseInt(primaryTierId),
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return post(endpoints.rules.secondaryTiers(rulesetId, ruleId), data, onSuccess, onFailure);
}

// Update an existing secondary rule tier entity via the rules API based on the given data
function updateSecondaryRuleTier(rulesetId, ruleId, tierId, primaryTierId, ordinal, taxRate, onSuccess, onFailure) {
    let data = {
        primary_tier_id: primaryTierId,
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return put(endpoints.rules.secondaryTiers(rulesetId, ruleId), tierId, data, onSuccess, onFailure);
}

// Delete a new secondary rule tier entity via the rules API based on the given secondary tier ID
function removeSecondaryRuleTier(rulesetId, ruleId, tierId, onSuccess, onFailure) {
    return remove(endpoints.rules.secondaryTiers(rulesetId, ruleId), tierId, onSuccess, onFailure);
}

if (typeof module != "undefined") module.exports = {
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
    removeSecondaryRuleTier,
    processBatch,
    updateRule
};