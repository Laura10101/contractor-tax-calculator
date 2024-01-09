/*
 * service_clients.js
 * Provides wrapper functions for easy access to required API endpoints
 */

/*
 * Helper functions for HTTP requests
 */
function queryToString(query) {
    queryString = "";
    for (const key in query) {
        if (query.hasOwnProperty(key)) {
            string += key + "=" + query[key];
        }
    }
    return queryString;
}

function url(endpoint) {
    return window.location.protocol + "//" + window.location.hostname + "/api/" + endpoint;
}

function query(endpoint, query, success, error) {
    url = url(endpoint);
    $.ajax({
        type: "GET",
        url: url + query == null ? "": "?" + queryToString(query),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function get(endpoint, id, success, error) {
    url = url(endpoint);
    $.ajax({
        type: "GET",
        url: url + id + "/",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function post(endpoint, data, success, error) {
    url = url(endpoint);
    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function put(endpoint, id, data, success, error) {
    url = url(endpoint);
    $.ajax({
        type: "PUT",
        url: url + id + "/",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function patch(endpoint, id, data, success, error) {
    url = url(endpoint);
    $.ajax({
        type: "PATCH",
        url: url + id + "/",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function remove(endpoint, id, success, error) {
    url = url(endpoint);
    $.ajax({
        type: "DELETE",
        url: url + id + "/",
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
    query(endpoints.jurisdictions.base, null, onSuccess, onFailure);
}

/*
 * Tax categories service client
 */
function getTaxCategories(onSuccess, onFailure) {
    query(endpoints.rules.taxCategories, null, onSuccess, onFailure);
}

/*
 * Forms service client
 */
function getFormForJurisdiction(jurisdictionId, onSuccess, onFailure) {
    query = {
        jurisdiction_ids: jurisdictionId
    }
    query(endpoints.forms.base, query, onSuccess, onFailure);
}

/*
 * Questions service client
 */
function createBooleanQuestion(formId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "boolean"
    };
    post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

function updateBooleanQuestion(formId, text, ordinal, explainer, isMandatory, questionId, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "boolean"
    };
    put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

function createNumericQuestion(formId, text, ordinal, explainer, isMandatory, isInteger, minValue, maxValue, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "numeric",
        is_integer: isInteger,
        min_value: minValue,
        max_value: maxValue
    };
    post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

function updateNumericQuestion(formId, questionId, text, ordinal, explainer, isMandatory, isInteger, minValue, maxValue, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "numeric",
        is_integer: isInteger,
        min_value: minValue,
        max_value: maxValue
    };
    put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

function createMultipleChoiceQuestion(formId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "multiple_choice"
    };
    post(endpoints.forms.questions(formId), data, onSuccess, onFailure);
}

function updateMultipleChoiceQuestion(formId, questionId, text, ordinal, explainer, isMandatory, onSuccess, onFailure) {
    data = {
        text: text,
        ordinal: ordinal,
        explainer: explainer,
        is_mandatory: isMandatory,
        type: "multiple_choice"
    };
    put(endpoints.forms.questions(formId), questionId, data, onSuccess, onFailure);
}

function deleteQuestion(formId, questionId, onSuccess, onFailure) {
    remove(endpoints.forms.questions(formId), questionId, onSuccess, onFailure);
}

/*
 * Multiple choice options service client
 */
function createMultipleChoiceOption(formId, questionId, text, explainer, onSuccess, onFailure) {
    data = {
        text: text,
        explainer: explainer
    }
    post(endpoints.forms.multipleChoiceOptions(formId, questionId), data, onSuccess, onFailure);
}

function deleteMultipleChoiceOption(formId, questionId, optionId, onSuccess, onFailure) {
    remove(endpoints.forms.multipleChoiceOptions(formId, questionId), optionId, onSuccess, onFailure);
}

/*
 * Rulesets service client
 */
function getRulesetsForJurisdiction(jurisdictionId, onSuccess, onFailure) {
    query = {
        jurisdiction_id: jurisdictionId
    };
    query(endpoints.rules.rulesets, query, onSuccess, onFailure);
}

function createRuleset(jurisdictionId, taxCategoryId, ordinal, onSuccess, onFailure) {
    data = {
        jurisdiction_id: jurisdictionId,
        tax_category_id: taxCategoryId,
        ordinal: ordinal
    };
    post(endpoints.rules.rulesets, data, onSuccess, onFailure);
}

function updateRuleset(rulesetId, jurisdictionId, taxCategoryId, ordinal, onSuccess, onFailure) {
    data = {
        jurisdiction_id: jurisdictionId,
        tax_category_id: taxCategoryId,
        ordinal: ordinal
    };
    put(endpoints.rules.rulesets, rulesetId, data, onSuccess, onFailure);
}

function deleteRuleset(rulesetId, onSuccess, onFailure) {
    remove(endpoints.rules.rulesets, rulesetId, onSuccess, onFailure);
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
        tax_rate: taxRate
    };
    post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

function updateFlatRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "flat_rate",
        tax_rate: taxRate
    };
    put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

function createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "tiered_rate"
    };
    post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

function updateTieredRateRule(rulesetId, name, explainer, variableName, ordinal, ruleId, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "tiered_rate"
    };
    put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

function createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, primaryRuleId, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "secondary_tiered_rate",
        primary_rule_id: primaryRuleId
    };
    post(endpoints.rules.rules(rulesetId), data, onSuccess, onFailure);
}

function updateSecondaryTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, primaryRuleId, onSuccess, onFailure) {
    data = {
        name: name,
        explainer: explainer,
        variable_name: variableName,
        ordinal: ordinal,
        type: "secondary_tiered_rate",
        primary_rule_id: primaryRuleId
    };
    put(endpoints.rules.rules(rulesetId), ruleId, data, onSuccess, onFailure);
}

function deleteRule(rulesetId, ruleId, onSuccess, onFailure) {
    remove(endpoints.rules.rules(rulesetId), ruleId, onSuccess, onFailure);
}

/*
 * Rule tiers service client
 */
function createRuleTier(rulesetId, ruleId, minValue, maxValue, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        min_value: minValue,
        max_value: maxValue,
        ordinal: ordinal,
        tax_rate: taxRate
    };
    post(endpoints.rules.tiers(rulesetId, ruleId), data, onSuccess, onFailure);
}

function updateRuleTier(rulesetId, ruleId, tierId, minValue, maxValue, ordinal, taxRate, onSuccess, onFailure) {
    data = {
        min_value: minValue,
        max_value: maxValue,
        ordinal: ordinal,
        tax_rate: taxRate
    };
    put(endpoints.rules.tiers(rulesetId, ruleId), tierId, data, onSuccess, onFailure);
}

function deleteRuleTier(rulesetId, ruleId, tierId, onSuccess, onFailure) {
    remove(endpoints.rules.rules(rulesetId, ruleId), tierId, onSuccess, onFailure);
}

/*
 * Secondary rule tiers service client
 */
function createSecondaryRuleTier(rulesetId, ruleId, primaryTierId, taxRate, onSuccess, onFailure) {
    data = {
        primary_tier_id: primaryTierId,
        tax_rate: taxRate
    };
    post(endpoints.rules.secondaryTiers(rulesetId, ruleId), data, onSuccess, onFailure);
}

function updateSecondaryRuleTier(rulesetId, ruleId, tierId, primaryTierId, taxRate, onSuccess, onFailure) {
    data = {
        primary_tier_id: primaryTierId,
        tax_rate: taxRate
    };
    put(endpoints.rules.secondaryTiers(rulesetId, ruleId), tierId, data, onSuccess, onFailure);
}

function deleteSecondaryRuleTier(rulesetId, ruleId, tierId, onSuccess, onFailure) {
    remove(endpoints.rules.secondaryTiers(rulesetId, ruleId), tierId, onSuccess, onFailure);
}