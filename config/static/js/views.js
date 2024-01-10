/*
 * views.js
 * Provides view functions to render views and react to view actions
 */

/*
 * Ruleset Views
 */
function displayRulesets(data) {
    app.jurisdictionRules = data;
    updateRulesetsDisplay(app.jurisdictionRules);
}

function displayRulesetsLoadError() {
    error("An error occurred while loading rulesets for selected jurisdiction.");
}


/*
 * Forms Views
 */
function displayQuestions(data) {
    app.jurisdictionForm = data;
    updateQuestionDisplay(app.jurisdictionForm.forms[Object.keys(app.jurisdictionForm.forms)[0]].questions);
}

function displayQuestionsLoadError() {
    error("An error occurred while loading questions for selected jurisdiction.");
}

/*
 * Jurisdiction Views
 */
function jurisdictionSelected() {
    jurisdictionId = getSelectedJurisdictionId();
    getFormForJurisdiction(jurisdictionId, displayQuestions, displayQuestionsLoadError);
    getRulesetsForJurisdiction(jurisdictionId, displayRulesets, displayRulesetsLoadError);
}

function loadJurisdictionSelect(data) {
    app.jurisdictions = data.jurisdictions;
    initJurisdictionsSelect(app.jurisdictions, jurisdictionSelected);
}

function displayJurisdictionLoadError() {
    error("An error occurred while loading jurisdictions.");
}

/*
 * Tax Category Views
 */
function loadTaxCategorySelect(data) {
    app.taxCategories = data;
}

function displayTaxCategoryLoadError() {
    error("An error occurred while loading tax categories.");
}

/*
 * Boolean Question Views
 */
function createBooleanQuestion() {

}

function editBooleanQuestion(id) {

}

function deleteBooleanQuestion(id) {

}

function moveBooleanQuestionUp(id) {

}

function moveBooleanQuestionDown(id) {
    
}

/*
 * Numeric Question Views
 */
function createNumericQuestion() {

}

function editNumericQuestion(id) {

}

function deleteNumericQuestion(id) {

}

function moveNumericQuestionUp(id) {

}

function moveNumericQuestionDown(id) {
    
}

/*
 * Multiple Choice Question Views
 */
function createMultipleChoiceQuestion() {

}

function editMultipleChoiceQuestion(id) {

}

function deleteMultipleChoiceQuestion(id) {

}

function moveMultipleChoiceQuestionUp(id) {

}

function moveMultipleChoiceQuestionDown(id) {
    
}

/*
 * Multiple Choice Option Views
 */

/*
 * Flat Rate Rule Views
 */

/*
 * Tiered Rate Rule Views
 */

/*
 * Rule Tier Views
 */

/*
 * Secondary Tiered Rate Rule Views
 */

/*
 * Secondary Rule Tier Views
 */

/*
 * Initialisation functions
 */
function init() {
    getJurisdictions(loadJurisdictionSelect, displayJurisdictionLoadError);
    getTaxCategories(loadTaxCategorySelect, displayTaxCategoryLoadError);
}

window.onload = init();