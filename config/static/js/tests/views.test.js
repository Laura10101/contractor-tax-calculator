const $ = require("jquery");
require("bootstrap");

const { 
    dialogStates,
    statusDialog,
    confirmationDialog,
    jurisdictionsSelect,
    questionTypeDialog,
    booleanQuestionDialog,
    numericQuestionDialog,
    multipleChoiceQuestionDialog,
    multipleChoiceOptionDialog,
    questionDisplayContainer,
    booleanQuestionDisplay,
    numericQuestionDisplay,
    multipleChoiceQuestionDisplay,
    rulesetDialog,
    ruleTypeDialog,
    flatRateRuleDialog,
    tieredRateRuleDialog,
    secondaryTieredRateRuleDialog,
    ruleTierDialog,
    secondaryRuleTierDialog,
    rulesetsDisplayContainer,
    rulesetDisplay,
    flatRateRuleDisplay,
    tieredRateRuleDisplay,
    secondaryTieredRateRuleDisplay
 } = require("../view_consts");

const { buildAppState } = require("./mocks/view_models.mocks.js");

const {
    app, findQuestionById, findRuleById, getRulesByTypeForJurisdiction, getQuestions, findParentRuleset, getTaxCategoryById, findPrimaryRuleTierById, setDialogState, setParentRuleset, setParentState
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
const { hasUncaughtExceptionCaptureCallback } = require("process");

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
    describe("Error views", () => {
        describe("Jurisdictions", () => {
            describe("Failure to load jurisdictions", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    displayJurisdictionLoadError();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while loading jurisdictions.");
                });
            });
        });

        describe("Tax categories", () => {
            describe("Failure to load tax categories", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    displayTaxCategoryLoadError();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while loading tax categories.");
                });
            });
        });

        describe("Questions", () => {
            describe("Failure to load questions", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    displayQuestionsLoadError();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while loading questions for selected jurisdiction.");
                });
            });
    
            describe("Failure to save question", () => {
    
            });
    
            describe("Failure to delete question", () => {
    
            });
        });

        describe("Multiple choice options", () => {
            describe("Failure to load multiple choice options", () => {
                test("should display an appropriate error", () => {
                    let question = findQuestionById(7);
                    expect(question).toBeDefined();
                    expect(question.id).toBe(7);

                    setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);

                    let dialogId = statusDialog.dialog.id;
                    displayMultipleChoiceOptionsError();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while refreshing multiple choice options for question " + app.dialogState.entity.name);
                });
            });
    
            describe("Failure to save multiple choice option", () => {
    
            });
    
            describe("Failure to delete multiple choice option", () => {
    
            });
        });

        describe("Rulesets", () => {
            describe("Failure to load rulesets", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    displayRulesetsLoadError();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while loading rulesets for selected jurisdiction.");
                });
            });

            describe("Failure to save ruleset", () => {

            });

            describe("Failure to delete ruleset", () => {

            });
        });

        describe("Rules", () => {          
            describe("Failure to save rule", () => {

            });

            describe("Failure to delete rule", () => {

            });
        });

        describe("Rule tiers", () => {
            describe("Failure to load rule tiers", () => {
                test("should display an appropriate error", () => {
                    let rule = findRuleById(44);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(44);

                    setParentState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);

                    let dialogId = statusDialog.dialog.id;
                    displayRuleTiersLoadedError();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while refreshing rule tiers for rule " + app.parentState.entity.name);
                });
            });

            describe("Failure to save rule tiers", () => {

            });

            describe("Failure to delete rule tiers", () => {

            });
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