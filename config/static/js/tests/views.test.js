const $ = require("jquery");
require("bootstrap");

const { buildAppState } = require("./mocks/view_models.mocks.js");

const {
    app, findQuestionById, findRuleById, getRulesByTypeForJurisdiction, getQuestions, findParentRuleset, getTaxCategoryById, findPrimaryRuleTierById
 } = require("../view_models");

const {
    displayQuestionsLoadError,
    displayJurisdictionLoadError,
    displayTaxCategoryLoadError,
    saveQuestionFailed,
    deleteQuestionFailed,
    displayMultipleChoiceOptionsError,
    saveMultipleChoiceOptionFailed,
    deleteMultipleChoiceOptionFailed,
    displayRulesetsLoadError,
    saveRulesetFailed,
    deleteRulesetFailed,
    saveRuleFailed,
    deleteRuleFailed,
    displayRuleTiersLoadedError,
    saveRuleTierFailed,
    deleteRuleTierFailed,
    confirmDeleteQuestion,
    confirmDeleteMultipleChoiceOption,
    displayQuestions,
    loadJurisdictionSelect,
    loadTaxCategorySelect,
    refreshQuestionsDisplay,
    questionTypeSelected,
    editQuestion,
    saveQuestionSucceeded,
    saveQuestion,
    deleteQuestionSucceeded,
    deleteQuestion,
    swapQuestionOrdinals,
    moveQuestionUp,
    moveQuestionDown,
    displayMultipleChoiceOptions,
    refreshMultipleChoiceOptionsDisplay,
    saveMultipleChoiceOptionSucceeded,
    saveMultipleChoiceOption,
    createMultipleChoiceOption,
    deleteMultipleChoiceOptionSucceeded,
    deleteMultipleChoiceOption,
    displayRulesets,
    refreshRulesetsDisplay,
    saveRulesetSucceeded,
    saveRuleset,
    createRuleset,
    deleteRulesetSucceeded,
    confirmDeleteRuleset,
    deleteRuleset,
    swapRulesetOrdinals,
    moveRulesetUp,
    moveRulesetDown,
    addRule,
    editRule,
    ruleTypeSelected,
    saveRuleSucceeded,
    saveRule,
    deleteRuleSucceeded,
    confirmDeleteRule,
    deleteRule,
    updateRuleOrdinal,
    swapRuleOrdinals,
    moveRuleUp,
    moveRuleDown,
    displayRuleTiersLoadedSucceeded,
    refreshRuleTiersDisplay,
    saveRuleTierSucceeded,
    saveRuleTier,
    createRuleTier,
    editRuleTier,
    saveRuleTierOrdinal,
    swapRuleTierOrdinals,
    moveRuleTierUp,
    moveRuleTierDown,
    deleteRuleTierSucceeded,
    confirmDeleteRuleTier,
    deleteRuleTier,
    init
} = require("../views");

// Helper functions
function isShown(dialogId) {
    // From Stackoverflow: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
    return $("#" + dialogId).data('bs.modal')?._isShown;
}

// Prepare state for tests
beforeEach(() => {
    // Set up DOM state
    // Used the following resource to load from a relative path:
    // https://ultimatecourses.com/blog/relative-paths-with-node-readfilesync
    let fs = require("fs");
    let path = require("path");
    let fileContents = fs.readFileSync(path.resolve(__dirname, "../../../templates/config/config.html"), "utf-8");
    document.open();
    document.write(fileContents);
    document.close();

    // Set up app state
    appState = buildAppState();
    app.jurisdictions = appState.jurisdictions;
    app.taxCategories = appState.taxCategories;
    app.jurisdictionForm = appState.jurisdictionForm;
    app.jurisdictionRules = appState.jurisdictionRules;
});


describe("Status views", () => {
    describe("Display errors", () => {
        test("should load", () => {
            expect(true).toBe(true);
        });
    });
});

describe("Jurisdiction views", () => {

});

describe("Tax category views", () => {

});

describe("Question views", () => {

});

describe("Multilple choice option views", () => {

});

describe("Ruleset views", () => {

});

describe("Rule views views", () => {

});

describe("Rule tier views views", () => {

});