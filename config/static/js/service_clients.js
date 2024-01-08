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

function query(url, query, success, error) {
    $.ajax({
        type: "GET",
        url: url + "?" + queryToString(query),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function get(url, id, success, error) {
    $.ajax({
        type: "GET",
        url: url + id + "/",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

function post(url, data, success, error) {
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

function put(url, id, data, success, error) {
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

function patch(url, id, data, success, error) {
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

function remove(url, id, success, error) {
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

}

/*
 * Tax categories service client
 */
function getTaxCategories(onSuccess, onFailure) {

}

/*
 * Forms service client
 */
function getFormForJurisdiction(jurisdictionId, onSuccess, onFailure) {

}

/*
 * Questions service client
 */
function createQuestion(onSuccess, onFailure) {

}

function updateQuestion(questionId, onSuccess, onFailure) {

}

function deleteQuestion(questionId, onSuccess, onFailure) {

}

/*
 * Multiple choice options service client
 */
function createMultipleChoiceOption(name, onSuccess, onFailure) {

}

function deleteMultipleChoiceOption(optionId, onSuccess, onFailure) {

}

/*
 * Rules service client
 */
function createRule(onSuccess, onFailure) {

}

function updateRule(questionId, onSuccess, onFailure) {

}

function deleteRule(questionId, onSuccess, onFailure) {

}

/*
 * Rule tiers service client
 */
function createRuleTier(onSuccess, onFailure) {

}

function updateRuleTier(tierId, onSuccess, onFailure) {

}

function deleteRuleTier(tierId, onSuccess, onFailure) {

}

/*
 * Secondary rule tiers service client
 */
function createSecondaryRuleTier(onSuccess, onFailure) {

}

function updateSecondaryRuleTier(tierId, onSuccess, onFailure) {

}

function deleteSecondaryRuleTier(tierId, onSuccess, onFailure) {
    
}