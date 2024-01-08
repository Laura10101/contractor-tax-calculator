/*
 * service_clients.js
 * Provides wrapper functions for easy access to required API endpoints
 */

/*
 * Helper functions for HTTP requests
 */
function queryToString(query) {

}

function httpError() {

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