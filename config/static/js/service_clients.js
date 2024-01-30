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

function queryToString(query) {
    queryString = "";
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

function toUrl(endpoint) {
    return app.apiHost.protocol + "//" + app.apiHost.hostname + "/api/" + endpoint;
}

function query(endpoint, query, success, error) {
    url = toUrl(endpoint);
    return $.ajax({
        type: "GET",
        url: query == null ? url: url + "?" + queryToString(query),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function get(endpoint, id, success, error) {
    url = toUrl(endpoint);
    return $.ajax({
        type: "GET",
        url: url + id + "/",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function post(endpoint, data, success, error) {
    url = toUrl(endpoint);
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

function put(endpoint, id, data, success, error) {
    url = toUrl(endpoint);
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

function patch(endpoint, id, data, success, error) {
    url = toUrl(endpoint);
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

function remove(endpoint, id, success, error) {
    url = toUrl(endpoint);
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

function getJurisdictions(onSuccess, onFailure) {
    return query(endpoints.jurisdictions.base, null, onSuccess, onFailure);
}

/*
 * Tax categories service client
 */
function getTaxCategories(onSuccess, onFailure) {
    return query(endpoints.rules.taxCategories, null, onSuccess, onFailure);
}

/*
 * Forms service client
 */
function getFormForJurisdiction(jurisdictionId, onSuccess, onFailure) {
    queryParameters = {
        jurisdiction_ids: jurisdictionId
    }
    return query(endpoints.forms.base, queryParameters, onSuccess, onFailure);
}

/*
 * Questions service client
 */
function createBooleanQuestion(formId, text, ordinal, explainer, variableName, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        variable_name: variableName,
        is_mandatory: isMandatory,
        type: "boolean"
    };
    return post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

function updateBooleanQuestion(formId, questionId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "boolean"
    };
    return put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

function createNumericQuestion(formId, text, ordinal, explainer, variableName, isMandatory, isInteger, minValue, maxValue, onSuccess, onFailure) {
    data = {
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

function updateNumericQuestion(formId, questionId, text, ordinal, explainer, isMandatory, isInteger, minValue, maxValue, onSuccess, onFailure) {
    data = {
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

function createMultipleChoiceQuestion(formId, text, ordinal, explainer, variableName, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        variable_name: variableName,
        is_mandatory: isMandatory,
        type: "multiple_choice"
    };
    return post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

function updateMultipleChoiceQuestion(formId, questionId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "multiple_choice"
    };
    return put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

function updateQuestion(question, onSuccess, onFailure) {
    formId = getFormId();
    switch (question.type) {
        case "boolean":
                return updateBooleanQuestion(formId, question.id, question.text, question.ordinal, question.explainer, question.is_mandatory, onSuccess, onFailure);
            break;
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
            break;
        case "multiple_choice":
                return updateMultipleChoiceQuestion(formId, question.id, question.text, question.ordinal, question.explainer, question.is_mandatory, onSuccess, onFailure);
            break;
    }
}

function removeQuestion(formId, questionId, onSuccess, onFailure) {
    return remove(endpoints.forms.questions(formId), questionId, onSuccess, onFailure);
}

/*
 * Multiple choice options service client
 */
function postMultipleChoiceOption(formId, questionId, text, explainer, onSuccess, onFailure) {
    data = {
        text: text,
        explainer: explainer
    }
    return post(endpoints.forms.multipleChoiceOptions(formId, questionId), data, onSuccess, onFailure);
}

function removeMultipleChoiceOption(formId, questionId, optionId, onSuccess, onFailure) {
    return remove(endpoints.forms.multipleChoiceOptions(formId, questionId), optionId, onSuccess, onFailure);
}

/*
 * Rulesets service client
 */
function getRulesetsForJurisdiction(jurisdictionId, onSuccess, onFailure) {
    queryParameters = {
        jurisdiction_id: jurisdictionId
    };
    return query(endpoints.rules.rulesets, queryParameters, onSuccess, onFailure);
}

function postRuleset(jurisdictionId, taxCategoryId, ordinal, onSuccess, onFailure) {
    data = {
        jurisdiction_id: parseInt(jurisdictionId),
        tax_category_id: parseInt(taxCategoryId),
        ordinal: ordinal
    };
    return post(endpoints.rules.rulesets, data, onSuccess, onFailure);
}

function patchRuleset(rulesetId, ordinal, onSuccess, onFailure) {
    data = {
        ordinal: ordinal
    };
    return patch(endpoints.rules.rulesets, rulesetId, data, onSuccess, onFailure);
}

function removeRuleset(rulesetId, onSuccess, onFailure) {
    return remove(endpoints.rules.rulesets, rulesetId, onSuccess, onFailure);
}

/*
 * Rules service client
 */
function createFlatRateRule(rulesetId, name, explainer, variableName, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "flat_rate",
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

function updateFlatRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "flat_rate",
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

function createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "tiered_rate"
    };
    return post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

function updateTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "tiered_rate"
    };
    return put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

function createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, primaryRuleId, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "secondary_tiered_rate",
        primary_rule_id: parseInt(primaryRuleId)
    };
    return post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

function updateSecondaryTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, primaryRuleId, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "secondary_tiered_rate",
        primary_rule_id: parseInt(primaryRuleId)
    };
    return put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

function removeRule(rulesetId, ruleId, onSuccess, onFailure) {
    return remove(endpoints.rules.rules(rulesetId), ruleId, onSuccess, onFailure);
}

/*
 * Rule tiers service client
 */
function postRuleTier(rulesetId, ruleId, minValue, maxValue, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        min_value: !isNaN(parseInt(minValue)) ? parseInt(minValue) : null,
        max_value: !isNaN(parseInt(maxValue)) ? parseInt(maxValue) : null,
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return post(endpoints.rules.tiers(rulesetId, ruleId), data, onSuccess, onFailure);
}

function updateRuleTier(rulesetId, ruleId, tierId, minValue, maxValue, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        min_value: !isNaN(parseInt(minValue)) ? parseInt(minValue) : null,
        max_value: !isNaN(parseInt(maxValue)) ? parseInt(maxValue) : null,
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return put(endpoints.rules.tiers(rulesetId, ruleId), tierId, data, onSuccess, onFailure);
}

function removeRuleTier(rulesetId, ruleId, tierId, onSuccess, onFailure) {
    return remove(endpoints.rules.tiers(rulesetId, ruleId), tierId, onSuccess, onFailure);
}

/*
 * Secondary rule tiers service client
 */
function postSecondaryRuleTier(rulesetId, ruleId, primaryTierId, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        primary_tier_id: parseInt(primaryTierId),
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return post(endpoints.rules.secondaryTiers(rulesetId, ruleId), data, onSuccess, onFailure);
}

function updateSecondaryRuleTier(rulesetId, ruleId, tierId, primaryTierId, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        primary_tier_id: primaryTierId,
        ordinal: ordinal,
        tax_rate: !isNaN(parseFloat(taxRate)) ? parseFloat(taxRate) : null
    };
    return put(endpoints.rules.secondaryTiers(rulesetId, ruleId), tierId, data, onSuccess, onFailure);
}

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
    removeSecondaryRuleTier
};