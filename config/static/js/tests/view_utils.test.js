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
    app
 } = require("../view_models");

const {
    showDialog,
    hideDialog,
    error,
    success,
    confirm,
    removeAllChildNodes,
    updateRuleTierTable,
    resetContainer,
    initJurisdictionsSelect,
    getSelectedJurisdictionId,
    displayCreateBooleanQuestionDialog,
    displayEditBooleanQuestionDialog,
    displayCreateNumericQuestionDialog,
    displayEditNumericQuestionDialog,
    updateMultipleChoiceQuestionDialogOptionsDisplay,
    displayCreateMultipleChoiceQuestionDialog,
    displayEditMultipleChoiceQuestionDialog,
    displayCreateMultipleChoiceOptionDialog,
    displayBooleanQuestion,
    displayNumericQuestion,
    displayMultipleChoiceQuestion,
    updateQuestionDisplay,
    displayCreateRulesetDialog,
    ruleTypeChosen,
    displayCreateFlatRateRuleDialog,
    displayEditFlatRateRuleDialog,
    displayCreateTieredRateRuleDialog,
    displayEditTieredRateRuleDialog,
    initPrimaryRulesSelect,
    displayCreateSecondaryTieredRateRuleDialog,
    displayEditSecondaryTieredRateRuleDialog,
    displayCreateRuleTierDialog,
    displayEditRuleTierDialog,
    initPrimaryRuleTiersSelect,
    displayCreateSecondaryRuleTierDialog,
    displayEditSecondaryRuleTierDialog,
    displayFlatRateRule,
    displayTieredRateRule,
    displaySecondaryTieredRateRule,
    displayRuleset,
    updateRulesetsDisplay
 } = require("../view_utils");


// Helper functions
function isShown(dialogId) {
    // From Stackoverflow: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
    return $("#" + dialogId).data('bs.modal')?._isShown;
}

function getDialogTitle(dialogConstants) {
    let container = document.getElementById(dialogConstants.label.id);
    return container.innerHTML;
}

function getDialogText(dialogConstants) {
    let container = document.getElementById(dialogConstants.message.id);
    return container.innerHTML;
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

describe("Dialog utilities", () => {
    describe("Helper functions", () => {
        describe("Show dialog", () => {
            test("should correctly display then hide status dialog", () => {
                let dialogId = statusDialog.dialog.id;
                showDialog(dialogId);
                expect(isShown(dialogId)).toBe(true);
                hideDialog(dialogId);
                expect(isShown(dialogId)).toBe(false);
            });
        });

        describe("Hide dialog", () => {

        });

    });

    describe("Status dialogs", () => {
        describe("Error dialog", () => {

        });

        describe("Success dialog", () => {

        });

        describe("Confirmation dialog", () => {

        });
    });

    describe("Question dialogs", () => {
        describe("Boolean question dialog", () => {
            describe("Create", () => {

            });

            describe("Edit", () => {

            });
        });

        describe("Numeric question dialog", () => {
            describe("Create", () => {

            });

            describe("Edit", () => {

            });
        });

        describe("Multiple choice question dialog", () => {
            describe("Create", () => {

            });

            describe("Edit", () => {

            });
        });
    });

    describe("Multiple choice option dialog", () => {
        describe("Create", () => {

        });

        describe("Edit", () => {

        });
    });

    describe("Ruleset dialog", () => {
        describe("Create", () => {

        });

        describe("Edit", () => {

        });
    });

    describe("Rule dialogs", () => {
        describe("Flat rate rule dialog", () => {
            describe("Create", () => {

            });

            describe("Edit", () => {

            });
        });

        describe("Tiered rate rule dialog", () => {
            describe("Create", () => {

            });

            describe("Edit", () => {

            });
        });

        describe("Secondary tiered rate rule dialog", () => {
            describe("Create", () => {

            });

            describe("Edit", () => {

            });
        });
    });

    describe("Rule tier dialogs", () => {
        describe("Create", () => {

        });

        describe("Edit", () => {

        });
    });
});

describe("Select utilities", () => {
    describe("Jurisdictions select", () => {
        describe("Initialisation", () => {

        });

        describe("Selection handler", () => {

        });
    });

    describe("Primary rule select", () => {
        describe("Initialisation", () => {

        });

        describe("Selection handler", () => {

        });
    });

    describe("Primary rule tiers select", () => {
        describe("Initialisation", () => {

        });

        describe("Selection handler", () => {

        });
    });
});

describe("Display utilities", () => {
    describe("Questions", () => {
        describe("List", () => {

        });

        describe("Boolean question", () => {

        });

        describe("Numeric question", () => {

        });

        describe("Multiple choice question", () => {

        });
    });

    describe("Multiple choice options", () => {

    });

    describe("Rulesets", () => {
        describe("List", () => {

        });

        describe("Ruleset", () => {

        });
    });

    describe("Rules", () => {
        describe("List", () => {

        });

        describe("Flat rate rule", () => {

        });

        describe("Tiered rate rule", () => {

        });

        describe("Secondary tiered rate rule", () => {

        });
    });

    describe("Rule tiers", () => {
        describe("Primary", () => {

        });

        describe("Secondary", () => {

        });
    });
});