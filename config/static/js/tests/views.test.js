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

 const {
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
} = require("../service_clients");

const { buildAppState } = require("./mocks/view_models.mocks.js");

const {
    app, findQuestionById, findRuleById, getRulesByTypeForJurisdiction, getQuestions, findParentRuleset, getTaxCategoryById, findPrimaryRuleTierById, setDialogState, setParentRuleset, setParentState
 } = require("../view_models");

const {
    doNothing,
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
const { showDialog, hideDialog, ruleTypeChosen, initJurisdictionsSelect } = require("../view_utils.js");

// Helper functions
function isShown(dialogId) {
    // From Stackoverflow: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
    return $("#" + dialogId).data('bs.modal')?._isShown;
}

beforeAll(() => {
    app.apiHost.protocol = "https:";
    app.apiHost.hostname = "8000-laura10101-contractorta-g5o2od5xoex.ws-eu107.gitpod.io";
    jest.useRealTimers();
});

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
    app.dialogState = {
        mode: null,
        entityType: null,
        entity: null
    };
    app.parentState = {
        mode: null,
        entityType: null,
        entity: null
    };
    app.parentRuleset = null;
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
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    saveQuestionFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to save question.");
                });
            });
    
            describe("Failure to delete question", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    deleteQuestionFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to delete question.");
                });
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
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    saveMultipleChoiceOptionFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to save multiple choice option.");
                });
            });
    
            describe("Failure to delete multiple choice option", () => {
                test("should display an appropriate error, move the app state to the dialog state and reshow the edit question dialog", () => {
                    let question = findQuestionById(7);
                    expect(question).toBeDefined();
                    expect(question.id).toBe(7);

                    setParentState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);
                    expect(app.parentState.entity).toEqual(question);

                    let dialogId = statusDialog.dialog.id;
                    deleteMultipleChoiceOptionFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to delete option.");

                    expect(app.dialogState.entity).toEqual(question);
                    expect(app.parentState.entity).toBeNull();

                    expect(isShown(multipleChoiceQuestionDialog.dialog.id)).toBe(true);
                });
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
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    saveRulesetFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to save ruleset.");
                });
            });

            describe("Failure to delete ruleset", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    deleteRulesetFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to delete ruleset.");
                });
            });
        });

        describe("Rules", () => {          
            describe("Failure to save rule", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    saveRuleFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to save rule.");
                });
            });

            describe("Failure to delete rule", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    deleteRuleFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to delete rule.");
                });
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

            describe("Failure to save rule tier", () => {
                test("should display an appropriate error", () => {
                    let dialogId = statusDialog.dialog.id;
                    saveRuleTierFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to save rule tier.");
                });
            });

            describe("Failure to delete rule tier", () => {
                test("should display an appropriate error and move app state to dialog state", () => {
                    let rule = findRuleById(44);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(44);

                    setParentState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);

                    let dialogId = statusDialog.dialog.id;
                    deleteRuleTierFailed();
                    expect(isShown(dialogId)).toBe(true);

                    let title = document.getElementById(statusDialog.label.id).innerHTML;
                    let message = document.getElementById(statusDialog.message.id).innerHTML;

                    expect(title).toBe("An Error Occurred");
                    expect(message).toBe("An error occurred while attempting to delete rule tier.");

                    expect(app.dialogState.entity).toEqual(rule);
                    expect(app.parentState.entity).toBeNull();
                });
            });
        });
    });

    describe("Confirmation views", () => {
        describe("Questions", () => {
            test("should display an appropriate confirmation dialog and correctly set the app state", () => {
                let question = findQuestionById(3);
                expect(question).toBeDefined();
                expect(question.id).toBe(3);

                let dialogId = confirmationDialog.dialog.id;
                deleteQuestion(question);
                expect(isShown(dialogId)).toBe(true);

                let title = document.getElementById(confirmationDialog.label.id).innerHTML;
                let message = document.getElementById(confirmationDialog.message.id).innerHTML;

                expect(title).toBe("Are you sure?");
                expect(message).toBe("Please confirm you wish for the following question to be deleted: " + question.text + ".");

                expect(app.dialogState.mode).toBe(dialogStates.modes.delete);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.question);
                expect(app.dialogState.entity).toEqual(question);
            });
        });

        describe("Multiple choice options", () => {
            test("should display an appropriate confirmation dialog and correctly set the app and parent states", () => {
                let question = findQuestionById(7);
                expect(question).toBeDefined();
                expect(question.id).toBe(7);

                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);

                option = {
                    "id": 798,
                    "text": "A made up option mock",
                    "explainer": "A completely fictional option"
                };

                let dialogId = confirmationDialog.dialog.id;
                deleteMultipleChoiceOption(option);
                expect(isShown(dialogId)).toBe(true);
                expect(isShown(multipleChoiceQuestionDialog.dialog.id)).toBe(false);

                let title = document.getElementById(confirmationDialog.label.id).innerHTML;
                let message = document.getElementById(confirmationDialog.message.id).innerHTML;

                expect(title).toBe("Are you sure?");
                expect(message).toBe("Please confirm you wish for the following option to be deleted: " + option.text + ".");

                expect(app.dialogState.mode).toBe(dialogStates.modes.delete);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.multipleChoiceOption);
                expect(app.dialogState.entity).toEqual(option);

                expect(app.parentState.mode).toBe(dialogStates.modes.edit);
                expect(app.parentState.entityType).toBe(dialogStates.entityTypes.multipleChoiceQuestion);
                expect(app.parentState.entity).toEqual(question);
            });
        });

        describe("Rulesets", () => {
            test("should display an appropriate confirmation dialog and correctly set the app state", () => {
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);

                let dialogId = confirmationDialog.dialog.id;
                deleteRuleset(ruleset);
                expect(isShown(dialogId)).toBe(true);

                let title = document.getElementById(confirmationDialog.label.id).innerHTML;
                let message = document.getElementById(confirmationDialog.message.id).innerHTML;

                expect(title).toBe("Are you sure?");
                expect(message).toBe("Please confirm you wish for the following ruleset to be deleted: " + ruleset.name + ".");

                expect(app.dialogState.mode).toBe(dialogStates.modes.delete);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.ruleset);
                expect(app.dialogState.entity).toEqual(ruleset);
            });
        });

        describe("Rules", () => {
            test("should display an appropriate confirmation dialog and correctly set the app state", () => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);

                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);

                let dialogId = confirmationDialog.dialog.id;
                deleteRule(ruleset, rule);

                expect(isShown(dialogId)).toBe(true);

                let title = document.getElementById(confirmationDialog.label.id).innerHTML;
                let message = document.getElementById(confirmationDialog.message.id).innerHTML;

                expect(title).toBe("Are you sure?");
                expect(message).toBe("Please confirm you wish for the following rule to be deleted: " + rule.name + ".");

                expect(app.dialogState.mode).toBe(dialogStates.modes.delete);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.rule);
                expect(app.dialogState.entity).toEqual(rule);

                expect(app.parentRuleset).toEqual(ruleset);
            });
        });

        describe("Rule tiers", () => {
            test("should display an appropriate confirmation dialog and correctly set the app state", () => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);

                let tier = rule.tiers[0];
                expect(tier).toBeDefined();
                expect(tier.id).toBe(3);

                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);

                let dialogId = confirmationDialog.dialog.id;
                deleteRuleTier(true, tier);

                expect(isShown(dialogId)).toBe(true);

                let title = document.getElementById(confirmationDialog.label.id).innerHTML;
                let message = document.getElementById(confirmationDialog.message.id).innerHTML;

                expect(title).toBe("Are you sure?");
                expect(message).toBe("Please confirm you wish for the selected rule tier to be deleted.");

                expect(app.dialogState.mode).toBe(dialogStates.modes.delete);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.ruleTier);
                expect(app.dialogState.entity).toEqual(tier);

                expect(app.parentState.mode).toBe(dialogStates.modes.edit);
                expect(app.parentState.entityType).toBe(dialogStates.entityTypes.tieredRateRule);
                expect(app.parentState.entity).toEqual(rule);
            });
        });
    });
});

describe("Jurisdiction views", () => {
    describe("Loading jurisdictions", () => {
        test("should correctly populate the jurisdictions select box and the app state", () => {
            data = {
                jurisdictions: app.jurisdictions
            };

            app.jurisdictions = null;

            loadJurisdictionSelect(data);

            expect(app.jurisdictions).toEqual(data.jurisdictions);

            let select = document.getElementById(jurisdictionsSelect.id);
            expect(select).toBeDefined();
            expect(select.options.length).toBe(app.jurisdictions.length);

            for (var i = 0; i < data.jurisdictions.length; i++) {
                expect(parseInt(select.options[i].value)).toBe(data.jurisdictions[i].id);
                expect(select.options[i].text).toBe(data.jurisdictions[i].name);
            }
        });
    });
});

describe("Tax category views", () => {
    describe("Loading tax categories", () => {
        test("should correctly populate the app state", () => {
            let taxCategories = app.taxCategories;
            app.taxCategories = null;

            loadTaxCategorySelect(taxCategories);

            expect(app.taxCategories).toEqual(taxCategories);
        });
    });
});

describe("Question views", () => {
    describe("Refreshing questions data", () => {
        test("should generate the correct request given the currently selected jurisdiction", done => {
            let selectedId = app.jurisdictions[0].id;
            initJurisdictionsSelect(app.jurisdictions, function() {});
            document.getElementById(jurisdictionsSelect.id).value = selectedId;

            function checkRequest(jurisdictionId, onSuccess, onFailure) {
                expect(parseInt(jurisdictionId)).toBe(selectedId);
                expect(onSuccess).toEqual(displayQuestions);
                expect(onFailure).toEqual(displayQuestionsLoadError);
                done();
            }

            refreshQuestionsDisplay(checkRequest);
        });
    });

    describe("Displaying questions", () => {
        test("should correctly populate the questions list and the app state", () => {
            let form = app.jurisdictionForm;
            app.jurisdictionForm = null;

            displayQuestions(form);

            expect(app.jurisdictionForm).toEqual(form);

            let questionDisplay = document.getElementById(questionDisplayContainer.id);
            expect(questionDisplay).toBeDefined();
            expect(questionDisplay.children.length).toBe(getQuestions().length + 3);
        });
    });

    describe("Creating questions", () => {
        describe("Choosing question type", () => {
            test("should display the correct dialog when boolean question is selected", () => {
                let questionTypeSelect = document.getElementById(questionTypeDialog.questionType.input.id);
                showDialog(questionTypeDialog.dialog.id);
                questionTypeSelect.value = "boolean";
                questionTypeSelected();
                expect(isShown(booleanQuestionDialog.dialog.id)).toBe(true);
                expect(isShown(questionTypeDialog.dialog.id)).toBe(false);
            });

            test("should display the correct dialog when numeric question is selected", () => {
                let questionTypeSelect = document.getElementById(questionTypeDialog.questionType.input.id);
                showDialog(questionTypeDialog.dialog.id);
                questionTypeSelect.value = "numeric";
                questionTypeSelected();
                expect(isShown(numericQuestionDialog.dialog.id)).toBe(true);
                expect(isShown(questionTypeDialog.dialog.id)).toBe(false);
            });

            test("should display the correct dialog when multiple choice question is selected", () => {
                let questionTypeSelect = document.getElementById(questionTypeDialog.questionType.input.id);
                showDialog(questionTypeDialog.dialog.id);
                questionTypeSelect.value = "multiple_choice";
                questionTypeSelected();
                expect(isShown(multipleChoiceQuestionDialog.dialog.id)).toBe(true);
                expect(isShown(questionTypeDialog.dialog.id)).toBe(false);
            });
        });
    });

    describe("Editing questions", () => {
        describe("Displaying edit dialog", () => {
            test("should display the correct dialog for a boolean question", () => {
                let question = findQuestionById(3);
                editQuestion(question);
                expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.booleanQuestion);
                expect(app.dialogState.entity).toEqual(question);
                expect(isShown(booleanQuestionDialog.dialog.id)).toBe(true);
            });

            test("should display the correct dialog for a numeric question", () => {
                let question = findQuestionById(4);
                editQuestion(question);
                expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.numericQuestion);
                expect(app.dialogState.entity).toEqual(question);
                expect(isShown(numericQuestionDialog.dialog.id)).toBe(true);
            });

            test("should display the correct dialog for a multiple choice question", () => {
                let question = findQuestionById(7);
                editQuestion(question);
                expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.multipleChoiceQuestion);
                expect(app.dialogState.entity).toEqual(question);
                expect(isShown(multipleChoiceQuestionDialog.dialog.id)).toBe(true);
            });
        });
    });

    describe("Deleting questions", () => {
        describe("Confirming deletion", () => {
            test("should hide confirmation dialog and trigger DELETE request", done => {
                let question = findQuestionById(3);

                function checkDeleteRequest(formId, questionId, success, failure) {
                    expect(questionId).toBe(question.id);
                    expect(isShown(confirmationDialog.dialog.id)).toBe(false);
                    done();
                }

                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.booleanQuestion, question);
                showDialog(confirmationDialog.dialog.id);
                confirmDeleteQuestion(checkDeleteRequest);
            });
        });

        describe("Successful deletion", () => {
            test("should show a success message, resequence ordinals, clear the app state, and refresh the questions display", done => {
                let nextOrdinal = 1;

                function checkOrdinalUpdate(question, success, failure) {
                    expect(question.ordinal).toBe(nextOrdinal);
                    nextOrdinal += 1;

                    expect(success).toEqual(doNothing);
                    expect(failure).toEqual(saveQuestionFailed);
                }

                function checkFinalAppState() {
                    expect(app.dialogState.mode).toBe(null);
                    expect(app.dialogState.entityType).toBe(null);
                    expect(app.dialogState.entity).toBe(null);
                    expect(isShown(statusDialog.dialog.id)).toBe(true);
                    done();
                }

                let question = findQuestionById(4);
                expect(question).toBeDefined();
                expect(question.id).toBe(4);

                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.numericQuestion, question);
                deleteQuestionSucceeded(null, null, null, checkOrdinalUpdate, checkFinalAppState);
            });
        });
    });

    describe("Reordering questions", () => {
        describe("Moving the top question up", () => {
            test("should do nothing", done => {
                let entity = findQuestionById(3);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(3);

                let updaterInvoked = false;

                function recordInvocation(updatedEntity, success, failure) {
                    updaterInvoked = true;
                    expect(success).toEqual(doNothing);
                    expect(failure).toEqual(saveQuestionFailed);
                }

                moveQuestionUp(entity, recordInvocation, done);
                expect(updaterInvoked).toBe(false);
                done();
            });
        });

        describe("Moving a question up", () => {
            test("should swap the ordinal of the selected question and the previous question and then refresh the questions display", done => {
                let entity = findQuestionById(4);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(4);

                let selectedEntityChecked = false;
                let previousEntityChecked = false

                function checkOrdinal(updatedEntity, success, failure) {
                    if (updatedEntity.id == 4) {
                        expect(updatedEntity.ordinal).toBe(1);
                        selectedEntityChecked = true;
                    } else if (updatedEntity.id == 3) {
                        expect(updatedEntity.ordinal).toBe(2);
                        previousEntityChecked = true;
                    }
                    expect(success).toEqual(doNothing);
                    expect(failure).toEqual(saveQuestionFailed);
                }

                moveQuestionUp(entity, checkOrdinal, done);
                expect(selectedEntityChecked && previousEntityChecked).toBe(true);
            });
        });

        describe("Moving a question down", () => {
            test("should swap the ordinal of the selected question and the next question and then refresh the questions display", done => {
                let entity = findQuestionById(4);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(4);

                let selectedEntityChecked = false;
                let nextEntityChecked = false

                function checkOrdinal(updatedEntity, success, failure) {
                    if (updatedEntity.id == 4) {
                        expect(updatedEntity.ordinal).toBe(3);
                        selectedEntityChecked = true;
                    } else if (updatedEntity.id == 7) {
                        expect(updatedEntity.ordinal).toBe(2);
                        nextEntityChecked = true;
                    }
                    expect(success).toEqual(doNothing);
                    expect(failure).toEqual(saveQuestionFailed);
                }

                moveQuestionDown(entity, checkOrdinal, done);
                expect(selectedEntityChecked && nextEntityChecked).toBe(true);
            });
        });

        describe("Moving the bottom question down", () => {
            test("should do nothing", done => {
                let entity = findQuestionById(7);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(7);

                let updaterInvoked = false;

                function recordInvocation(updatedEntity, success, failure) {
                    updaterInvoked = true;
                    expect(success).toEqual(doNothing);
                    expect(failure).toEqual(saveQuestionFailed);
                }

                moveQuestionDown(entity, recordInvocation, done);
                expect(updaterInvoked).toBe(false);
                done();
            });
        });
    });
});

describe("Multilple choice option views", () => {
    describe("Refreshing multiple choice options data", () => {
        test("should generate the correct request given the currently selected jurisdiction", done => {
            let selectedId = app.jurisdictions[0].id;
            initJurisdictionsSelect(app.jurisdictions, function() {});
            document.getElementById(jurisdictionsSelect.id).value = selectedId;

            function checkRequest(jurisdictionId, onSuccess, onFailure) {
                expect(parseInt(jurisdictionId)).toBe(selectedId);
                expect(onSuccess).toEqual(displayMultipleChoiceOptions);
                expect(onFailure).toEqual(displayMultipleChoiceOptionsError);
                done();
            }

            refreshMultipleChoiceOptionsDisplay(checkRequest);
        });
    });

    describe("Displaying multiple choice options", () => {
        test("should correctly populate the options display when the question is held in the app state", () => {
            let question = findQuestionById(7);
            expect(question).toBeDefined();
            expect(question.id).toBe(7);
            expect(question.options).toBeDefined();

            setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);
            
            let form = app.jurisdictionForm;
            app.jurisdictionForm = null;

            displayMultipleChoiceOptions(form);

            expect(app.jurisdictionForm).toBe(form);

            expect(app.dialogState.entity).toBe(question);
            
            let optionsTable = document.getElementById(multipleChoiceQuestionDialog.options.table.id);
            expect(optionsTable).toBeDefined();
            expect(optionsTable.children.length).toBe(question.options.length + 1);
        });

        test("should correctly populate the options display when the question is held in the parent state", () => {
            let question = findQuestionById(7);
            expect(question).toBeDefined();
            expect(question.id).toBe(7);
            expect(question.options).toBeDefined();

            setParentState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);
            
            let form = app.jurisdictionForm;
            app.jurisdictionForm = null;

            displayMultipleChoiceOptions(form);

            expect(app.jurisdictionForm).toEqual(form);

            expect(app.dialogState.entity).toEqual(question);
            
            let optionsTable = document.getElementById(multipleChoiceQuestionDialog.options.table.id);
            expect(optionsTable).toBeDefined();
            expect(optionsTable.children.length).toBe(question.options.length + 1);
        });
    });

    describe("Creating multiple choice options", () => {
        test("should display the correct dialog and move the app state to the parent state", () => {
            let question = findQuestionById(7);
            setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);
            
            createMultipleChoiceOption();
            
            expect(app.parentState.mode).toBe(dialogStates.modes.edit);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.multipleChoiceQuestion);
            expect(app.parentState.entity).toEqual(question);
            expect(isShown(multipleChoiceOptionDialog.dialog.id)).toBe(true);
        });
    });

    describe("Deleting multiple choice options", () => {
        describe("Confirming deletion", () => {
            test("should hide confirmation dialog and trigger DELETE request", done => {
                let question = findQuestionById(3);
                let option = {
                    id: 7
                };

                function checkDeleteRequest(formId, questionId, optionId, success, failure) {
                    expect(questionId).toBe(question.id);
                    expect(optionId).toBe(option.id);
                    expect(isShown(confirmationDialog.dialog.id)).toBe(false);
                    done();
                }

                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.multipleChoiceOption, option);
                setParentState(dialogStates.modes.edit, dialogStates.entityTypes.multipleChoiceQuestion, question);
                showDialog(confirmationDialog.dialog.id);
                confirmDeleteMultipleChoiceOption(checkDeleteRequest);
            });
        });

        describe("Successful deletion", () => {
            test("should reshow the multiple choice question dialog and refresh the multiple choice options display", done => {
                function checkFinalAppState() {
                    expect(isShown(multipleChoiceQuestionDialog.dialog.id)).toBe(true);
                    done();
                }
                deleteMultipleChoiceOptionSucceeded(null, null, null, checkFinalAppState);
            });
        });
    });
});

describe("Ruleset views", () => {
    describe("Refreshing rulesets data", () => {
        test("should generate the correct request given the currently selected jurisdiction", done => {
            let selectedId = app.jurisdictions[0].id;
            initJurisdictionsSelect(app.jurisdictions, function() {});
            document.getElementById(jurisdictionsSelect.id).value = selectedId;

            function checkRequest(jurisdictionId, onSuccess, onFailure) {
                expect(parseInt(jurisdictionId)).toBe(selectedId);
                expect(onSuccess).toEqual(displayRulesets);
                expect(onFailure).toEqual(displayRulesetsLoadError);
                done();
            }

            refreshRulesetsDisplay(checkRequest);
        });
    });

    describe("Displaying rulesets", () => {
        test("should correctly populate the rulesets display and set the app state", () => {
            let rulesets = app.jurisdictionRules;
            app.jurisdictionRules = null;

            let rulesetsDisplay = document.getElementById(rulesetsDisplayContainer.id);
            expect(rulesetsDisplay.children.length).toBe(1);

            displayRulesets(rulesets);

            expect(app.jurisdictionRules).toEqual(rulesets);
            expect(rulesetsDisplay).toBeDefined();
            expect(rulesetsDisplay.children.length).toBe(rulesets.length + 1);

            for (var i = 0; i < rulesets.length; i++) {
                let ruleset = rulesets[i];
                let rulesetCard = rulesetsDisplay.children[i + 1];
                expect(rulesetCard).toBeDefined();

                let rule = ruleset.rules[i];
                let rulesDisplay = rulesetCard.querySelector("#" + rulesetDisplay.rules.id + "-" + ruleset.id);
                expect(rulesDisplay).toBeDefined();
                expect(rulesDisplay.children.length).toBe(ruleset.rules.length + 3);
            }
        });
    });

    describe("Creating rulesets", () => {
        test("should display the create ruleset dialog and set the app state appropriately", () => {
            createRuleset();
            expect(isShown(rulesetDialog.dialog.id)).toBe(true);
            expect(app.dialogState.mode).toBe(dialogStates.modes.create);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.ruleset);
            expect(app.dialogState.entity).toBe(null);
        });
    });

    describe("Deleting rulesets", () => {
        describe("Confirming deletion", () => {
            test("should hide confirmation dialog and trigger DELETE request", done => {
                let ruleset = findParentRuleset(45);

                function checkDeleteRequest(rulesetId, success, failure) {
                    expect(rulesetId).toBe(ruleset.id);                    
                    expect(isShown(confirmationDialog.dialog.id)).toBe(false);
                    done();
                }

                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleset, ruleset);
                showDialog(confirmationDialog.dialog.id);
                confirmDeleteRuleset(checkDeleteRequest);
            });
        });

        describe("Successful deletion", () => {
            test("should show a success message, resequence ordinals, clear the app state, and refresh the rulesets display", done => {
                let nextOrdinal = 1;
    
                function checkOrdinalUpdate(id, ordinal, success, failure) {
                    expect(ordinal).toBe(nextOrdinal);
                    nextOrdinal += 1;
    
                    expect(success).toEqual(doNothing);
                    expect(failure).toEqual(saveRulesetFailed);
                }
    
                function checkFinalAppState() {
                    expect(app.dialogState.mode).toBe(null);
                    expect(app.dialogState.entityType).toBe(null);
                    expect(app.dialogState.entity).toBe(null);
                    expect(isShown(statusDialog.dialog.id)).toBe(true);
                    done();
                }
    
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
    
                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleset, ruleset);
                deleteRulesetSucceeded(checkOrdinalUpdate, checkFinalAppState);
            });
        });
    });
});

describe("Rule views views", () => {
    describe("Creating rules", () => {
        describe("Choosing to add rule", () => {
            test("should display choose rule type dialog and set parent ruleset", () => {
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                addRule(ruleset);

                expect(app.parentRuleset).toEqual(ruleset);
                expect(isShown(ruleTypeDialog.dialog.id)).toBe(true);
            });
        });

        describe("Choosing a rule type", () => {
            test("should display the flat rate rule dialog when flat rate rule chosen", () => {
                showDialog(ruleTypeDialog.dialog.id);
                let select = document.getElementById(ruleTypeDialog.ruleType.input.id);
                select.value = "flat_rate";
                ruleTypeSelected();
                expect(app.dialogState.mode).toBe(dialogStates.modes.create);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.flatRateRule);
                expect(app.dialogState.entity).toBe(null);
                expect(isShown(flatRateRuleDialog.dialog.id)).toBe(true);
                expect(isShown(ruleTypeDialog.dialog.id)).toBe(false);
            });

            test("should display the tiered rate rule dialog when tiered rate rule chosen", () => {
                showDialog(ruleTypeDialog.dialog.id);
                let select = document.getElementById(ruleTypeDialog.ruleType.input.id);
                select.value = "tiered_rate";
                ruleTypeSelected();
                expect(app.dialogState.mode).toBe(dialogStates.modes.create);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.tieredRateRule);
                expect(app.dialogState.entity).toBe(null);
                expect(isShown(tieredRateRuleDialog.dialog.id)).toBe(true);
                expect(isShown(ruleTypeDialog.dialog.id)).toBe(false);
            });

            test("should display the secondary tiered rate rule dialog when secondary tiered rate rule chosen", () => {
                showDialog(ruleTypeDialog.dialog.id);
                let select = document.getElementById(ruleTypeDialog.ruleType.input.id);
                select.value = "secondary_tiered_rate";
                ruleTypeSelected();
                expect(app.dialogState.mode).toBe(dialogStates.modes.create);
                expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.secondaryTieredRateRule);
                expect(app.dialogState.entity).toBe(null);
                expect(isShown(secondaryTieredRateRuleDialog.dialog.id)).toBe(true);
                expect(isShown(ruleTypeDialog.dialog.id)).toBe(false);
            });
        });
    });

    describe("Editing rules", () => {
        test("should display the flat rate rule dialog when flat rate rule given", () => {
            let rule = findRuleById(41);
            let ruleset = findParentRuleset(41);
            expect(ruleset).toBeDefined();
            editRule(ruleset, rule);
            expect(app.parentRuleset).toEqual(ruleset);
            expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.flatRateRule);
            expect(app.dialogState.entity).toEqual(rule);
            expect(isShown(flatRateRuleDialog.dialog.id)).toBe(true);
        });

        test("should display the tiered rate rule dialog when tiered rate rule given", () => {
            let rule = findRuleById(44);
            let ruleset = findParentRuleset(44);
            expect(ruleset).toBeDefined();
            editRule(ruleset, rule);
            expect(app.parentRuleset).toEqual(ruleset);
            expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.tieredRateRule);
            expect(app.dialogState.entity).toEqual(rule);
            expect(isShown(tieredRateRuleDialog.dialog.id)).toBe(true);
        });

        test("should display the secondary tiered rate rule dialog when secondary tiered rate rule given", () => {
            let rule = findRuleById(45);
            let ruleset = findParentRuleset(45);
            expect(ruleset).toBeDefined();
            editRule(ruleset, rule);
            expect(app.parentRuleset).toEqual(ruleset);
            expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.secondaryTieredRateRule);
            expect(app.dialogState.entity).toEqual(rule);
            expect(isShown(secondaryTieredRateRuleDialog.dialog.id)).toBe(true);
        });
    });

    describe("Deleting rules", () => {
        describe("Confirming deletion", () => {
            test("should hide confirmation dialog and trigger DELETE request", done => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();

                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);

                function checkDeleteRequest(rulesetId, ruleId, success, failure) {
                    expect(rulesetId).toBe(ruleset.id);
                    expect(ruleId).toBe(rule.id);
                    expect(success).toBe(deleteRuleSucceeded);
                    expect(failure).toBe(deleteRuleFailed);
                    expect(isShown(confirmationDialog.dialog.id)).toBe(false);
                    done();
                }

                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.tieredRateRule, rule);
                setParentRuleset(ruleset);
                showDialog(confirmationDialog.dialog.id);
                confirmDeleteRule(checkDeleteRequest);
            });
        });

        describe("Successful deletion", () => {
            describe("of a flat rate rule", () => {
                test("should show a success message, resequence ordinals, clear the app state, and refresh the rules display", done => {
                    let nextOrdinal = 1;
        
                    function checkFlatRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, taxRate, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
    
                    function checkTieredRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
    
                    function checkSecondaryTieredRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, primaryRuleId, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
        
                    function checkFinalAppState() {
                        expect(app.dialogState.mode).toBe(null);
                        expect(app.dialogState.entityType).toBe(null);
                        expect(app.dialogState.entity).toBe(null);
                        expect(isShown(statusDialog.dialog.id)).toBe(true);
                        done();
                    }
        
                    let rule = findRuleById(41);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(41);
                    expect(rule.type).toBe("flat_rate");
    
                    setParentRuleset(findParentRuleset(41));
        
                    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.flatRateRule, rule);
                    deleteRuleSucceeded(checkFlatRateOrdinalUpdate, checkTieredRateOrdinalUpdate, checkSecondaryTieredRateOrdinalUpdate, checkFinalAppState);
                });
            });
    
            describe("of a tiered rate rule", () => {
                test("should show a success message, resequence ordinals, clear the app state, and refresh the rules display", done => {
                    let nextOrdinal = 1;
        
                    function checkFlatRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, taxRate, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
    
                    function checkTieredRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
    
                    function checkSecondaryTieredRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, primaryRuleId, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
        
                    function checkFinalAppState() {
                        expect(app.dialogState.mode).toBe(null);
                        expect(app.dialogState.entityType).toBe(null);
                        expect(app.dialogState.entity).toBe(null);
                        expect(isShown(statusDialog.dialog.id)).toBe(true);
                        done();
                    }
        
                    let rule = findRuleById(44);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(44);
                    expect(rule.type).toBe("tiered_rate");
    
                    setParentRuleset(findParentRuleset(44));
        
                    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.flatRateRule, rule);
                    deleteRuleSucceeded(checkFlatRateOrdinalUpdate, checkTieredRateOrdinalUpdate, checkSecondaryTieredRateOrdinalUpdate, checkFinalAppState);
                });
            });
    
            describe("of a secondary tiered rate rule", () => {
                test("should show a success message, resequence ordinals, clear the app state, and refresh the rules display", done => {
                    let nextOrdinal = 1;
        
                    function checkFlatRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, taxRate, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
    
                    function checkTieredRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
    
                    function checkSecondaryTieredRateOrdinalUpdate(rulesetId, ruleId, name, explainer, varName, ordinal, primaryRuleId, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleFailed);
                    }
        
                    function checkFinalAppState() {
                        expect(app.dialogState.mode).toBe(null);
                        expect(app.dialogState.entityType).toBe(null);
                        expect(app.dialogState.entity).toBe(null);
                        expect(isShown(statusDialog.dialog.id)).toBe(true);
                        done();
                    }
        
                    let rule = findRuleById(45);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(45);
                    expect(rule.type).toBe("secondary_tiered_rate");
    
                    setParentRuleset(findParentRuleset(45));
        
                    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.flatRateRule, rule);
                    deleteRuleSucceeded(checkFlatRateOrdinalUpdate, checkTieredRateOrdinalUpdate, checkSecondaryTieredRateOrdinalUpdate, checkFinalAppState);
                });
            });
        });
    });

    describe("Reordering rules", () => {
        describe("Moving the top rule up", () => {
            test("should do nothing", done => {
                let entity = findRuleById(41);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(41);

                let parent = findParentRuleset(41);
                expect(parent).toBeDefined();

                let updaterInvoked = false;

                function recordInvocation(ruleset, updatedEntity) {
                    updaterInvoked = true;
                }

                moveRuleUp(parent, entity, recordInvocation, done);
                expect(updaterInvoked).toBe(false);
                done();
            });
        });

        describe("Moving a rule up", () => {
            test("should swap the ordinal of the selected rule and the previous rule and then refresh the rule display", done => {
                let entity = findRuleById(44);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(44);

                let parent = findParentRuleset(44);
                expect(parent).toBeDefined();

                let selectedEntityChecked = false;
                let previousEntityChecked = false

                function checkOrdinal(ruleset, updatedEntity) {
                    if (updatedEntity.id == 44) {
                        expect(updatedEntity.ordinal).toBe(1);
                        selectedEntityChecked = true;
                    } else if (updatedEntity.id == 41) {
                        expect(updatedEntity.ordinal).toBe(2);
                        previousEntityChecked = true;
                    }
                }

                moveRuleUp(parent, entity, checkOrdinal, done);
                expect(selectedEntityChecked && previousEntityChecked).toBe(true);
            });
        });

        describe("Moving a rule down", () => {
            test("should swap the ordinal of the selected rule and the next rule and then refresh the rules display", done => {
                let entity = findRuleById(44);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(44);

                let parent = findParentRuleset(44);
                expect(parent).toBeDefined();

                let selectedEntityChecked = false;
                let nextEntityChecked = false

                function checkOrdinal(ruleset, updatedEntity) {
                    if (updatedEntity.id == 44) {
                        expect(updatedEntity.ordinal).toBe(3);
                        selectedEntityChecked = true;
                    } else if (updatedEntity.id == 45) {
                        expect(updatedEntity.ordinal).toBe(2);
                        nextEntityChecked = true;
                    }
                }

                moveRuleDown(parent, entity, checkOrdinal, done);
                expect(selectedEntityChecked && nextEntityChecked).toBe(true);
            });
        });

        describe("Moving the bottom rule down", () => {
            test("should do nothing", done => {
                let entity = findRuleById(45);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(45);

                let parent = findParentRuleset(45);
                expect(parent).toBeDefined();

                let updaterInvoked = false;

                function recordInvocation(ruleset, updatedEntity) {
                    updaterInvoked = true;
                }

                moveRuleDown(parent, entity, recordInvocation, done);
                expect(updaterInvoked).toBe(false);
                done();
            });
        });
    });
});

describe("Rule tier views views", () => {
    describe("Refreshing rule tier data", () => {
        test("should generate the correct request given the currently selected jurisdiction", done => {
            let selectedId = app.jurisdictions[0].id;
            initJurisdictionsSelect(app.jurisdictions, function() {});
            document.getElementById(jurisdictionsSelect.id).value = selectedId;

            function checkRequest(jurisdictionId, onSuccess, onFailure) {
                expect(parseInt(jurisdictionId)).toBe(selectedId);
                expect(onSuccess).toEqual(displayRuleTiersLoadedSucceeded);
                expect(onFailure).toEqual(displayRuleTiersLoadedError);
                done();
            }

            refreshRuleTiersDisplay(checkRequest);
        });
    });

    describe("Displaying rule tiers", () => {
        describe("Primary rule tiers", () => {
            test("should correctly populate the rule tiers display and set the app state when the rule is in the app state", () => {
                let rule = findRuleById(44);
                let rulesets = app.jurisdictionRules;
                app.jurisdictionRules = null;

                expect(rule).toBeDefined();
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);
    
                displayRuleTiersLoadedSucceeded(rulesets);

                expect(app.jurisdictionRules).toEqual(rulesets);
                expect(app.dialogState.entity).toEqual(rule);

                let display = document.getElementById(tieredRateRuleDialog.tiers.table.id);
                expect(display).toBeDefined();
                expect(display.children.length).toBe(rule.tiers.length + 1);
            });

            test("should correctly populate the rule tiers display and set the app state when the rule is in the parent state", () => {
                let rule = findRuleById(44);
                let rulesets = app.jurisdictionRules;
                app.jurisdictionRules = null;

                expect(rule).toBeDefined();
                setParentState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);
    
                displayRuleTiersLoadedSucceeded(rulesets);

                expect(app.jurisdictionRules).toEqual(rulesets);
                expect(app.dialogState.entity).toEqual(rule);

                let display = document.getElementById(tieredRateRuleDialog.tiers.table.id);
                expect(display).toBeDefined();
                expect(display.children.length).toBe(rule.tiers.length + 1);
            });
        });

        describe("Secondary rule tiers", () => {
            test("should correctly populate the secondary rule tiers display and set the app state when the rule is in the app state", () => {
                let rule = findRuleById(45);
                let rulesets = app.jurisdictionRules;
                app.jurisdictionRules = null;

                expect(rule).toBeDefined();
                setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryTieredRateRule, rule);
    
                displayRuleTiersLoadedSucceeded(rulesets);

                expect(app.jurisdictionRules).toEqual(rulesets);
                expect(app.dialogState.entity).toEqual(rule);

                let display = document.getElementById(secondaryTieredRateRuleDialog.tiers.table.id);
                expect(display).toBeDefined();
                expect(display.children.length).toBe(rule.tiers.length + 1);
            });

            test("should correctly populate the secondary rule tiers display and set the app state when the rule is in the parent state", () => {
                let rule = findRuleById(45);
                let rulesets = app.jurisdictionRules;
                app.jurisdictionRules = null;

                expect(rule).toBeDefined();
                setParentState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryTieredRateRule, rule);
    
                displayRuleTiersLoadedSucceeded(rulesets);

                expect(app.jurisdictionRules).toEqual(rulesets);
                expect(app.dialogState.entity).toEqual(rule);

                let display = document.getElementById(secondaryTieredRateRuleDialog.tiers.table.id);
                expect(display).toBeDefined();
                expect(display.children.length).toBe(rule.tiers.length + 1);
            });
        });
    });

    describe("Creating primary rule tiers", () => {
        test("should display the create rule tier dialog and correctly set app state", () => {
            let rule = findRuleById(44);
            expect(rule).toBeDefined();
            expect(rule.id).toBe(44);

            setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);
            createRuleTier(true);
            
            // Check app state
            expect(app.dialogState.mode).toBe(dialogStates.modes.create);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.ruleTier);
            expect(app.dialogState.entity).toBe(null);

            // Check parent state
            expect(app.parentState.mode).toBe(dialogStates.modes.edit);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.tieredRateRule);
            expect(app.parentState.entity).toBe(rule);

            // Check the dialog
            expect(isShown(ruleTierDialog.dialog.id)).toBe(true);
        });
    });

    describe("Creating secondary rule tiers", () => {
        test("should display the create secondary rule tier dialog and correctly set app state", () => {
            let rule = findRuleById(45);
            expect(rule).toBeDefined();
            expect(rule.id).toBe(45);

            setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryTieredRateRule, rule);
            createRuleTier(false);
            
            // Check app state
            expect(app.dialogState.mode).toBe(dialogStates.modes.create);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.secondaryRuleTier);
            expect(app.dialogState.entity).toBe(null);

            // Check parent state
            expect(app.parentState.mode).toBe(dialogStates.modes.edit);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.secondaryTieredRateRule);
            expect(app.parentState.entity).toBe(rule);

            // Check the dialog
            expect(isShown(secondaryRuleTierDialog.dialog.id)).toBe(true);
        });
    });

    describe("Editing primary rule tiers", () => {
        test("should display the edit rule tier dialog and correctly set app state", () => {
            let rule = findRuleById(44);
            expect(rule).toBeDefined();
            expect(rule.id).toBe(44);

            let tier = rule.tiers[0];
            expect(tier).toBeDefined();

            setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);
            editRuleTier(true, tier);
            
            // Check app state
            expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.ruleTier);
            expect(app.dialogState.entity).toBe(tier);

            // Check parent state
            expect(app.parentState.mode).toBe(dialogStates.modes.edit);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.tieredRateRule);
            expect(app.parentState.entity).toBe(rule);

            // Check the dialog
            expect(isShown(ruleTierDialog.dialog.id)).toBe(true);
        });
    });

    describe("Editing secondary rule tiers", () => {
        test("should display the edit secondary rule tier dialog and correctly set app state", () => {
            let rule = findRuleById(45);
            expect(rule).toBeDefined();
            expect(rule.id).toBe(45);

            let tier = rule.tiers[0];
            expect(tier).toBeDefined();

            setDialogState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryTieredRateRule, rule);
            editRuleTier(false, tier);
            
            // Check app state
            expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.secondaryRuleTier);
            expect(app.dialogState.entity).toBe(tier);

            // Check parent state
            expect(app.parentState.mode).toBe(dialogStates.modes.edit);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.secondaryTieredRateRule);
            expect(app.parentState.entity).toBe(rule);

            // Check the dialog
            expect(isShown(secondaryRuleTierDialog.dialog.id)).toBe(true);
        });
    });

    describe("Deleting rule tiers", () => {
        describe("Confirming deletion", () => {
            test("should hide confirmation dialog and trigger DELETE request", done => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();

                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);

                let tier = rule.tiers[1];
                expect(tier).toBeDefined();

                function checkDeleteRequest(rulesetId, ruleId, tierId, success, failure) {
                    expect(rulesetId).toBe(ruleset.id);
                    expect(ruleId).toBe(rule.id);
                    expect(tierId).toBe(tier.id);
                    expect(success).toBe(deleteRuleTierSucceeded);
                    expect(failure).toBe(deleteRuleTierFailed);
                    expect(isShown(confirmationDialog.dialog.id)).toBe(false);
                    done();
                }

                setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleTier, tier);
                setParentState(dialogStates.modes.delete, dialogStates.entityTypes.tieredRateRule, rule);
                showDialog(confirmationDialog.dialog.id);
                confirmDeleteRuleTier(checkDeleteRequest, checkDeleteRequest);
            });
        });

        describe("Successful deletion", () => {
            describe("of a rule tier", () => {
                test("should show a success message, resequence ordinals, clear the app state, and refresh the tiers display", done => {
                    let nextOrdinal = 1;
        
                    function checkOrdinalUpdate(rulesetId, ruleId, tierId, minValue, maxValue, ordinal, taxRate, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleTierFailed);
                    }
        
                    function checkFinalAppState() {
                        expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
                        expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.tieredRateRule);
                        expect(app.dialogState.entity).toEqual(rule);
                        expect(isShown(statusDialog.dialog.id)).toBe(true);
                        done();
                    }
        
                    let rule = findRuleById(44);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(44);
                    expect(rule.type).toBe("tiered_rate");
    
                    setParentState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, rule);
                    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.ruleTier, rule.tiers[2]);
    
                    deleteRuleTierSucceeded(checkOrdinalUpdate, checkOrdinalUpdate, checkFinalAppState);
                });
            });
    
            describe("of a secondary rule tier", () => {
                test("should show a success message, resequence ordinals, clear the app state, and refresh the tiers display", done => {
                    let nextOrdinal = 1;
        
                    function checkOrdinalUpdate(rulesetId, ruleId, tierId, primaryTierId, ordinal, taxRate, success, failure) {
                        expect(ordinal).toBe(nextOrdinal);
                        nextOrdinal += 1;
        
                        expect(success).toEqual(doNothing);
                        expect(failure).toEqual(saveRuleTierFailed);
                    }
        
                    function checkFinalAppState() {
                        expect(app.dialogState.mode).toBe(dialogStates.modes.edit);
                        expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.secondaryTieredRateRule);
                        expect(app.dialogState.entity).toEqual(rule);
                        expect(isShown(statusDialog.dialog.id)).toBe(true);
                        done();
                    }
        
                    let rule = findRuleById(45);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(45);
                    expect(rule.type).toBe("secondary_tiered_rate");
    
                    setParentState(dialogStates.modes.edit, dialogStates.entityTypes.secondaryTieredRateRule, rule);
                    setDialogState(dialogStates.modes.delete, dialogStates.entityTypes.secondaryRuleTier, rule.tiers[0]);
    
                    deleteRuleTierSucceeded(checkOrdinalUpdate, checkOrdinalUpdate, checkFinalAppState);
                });
            });
        });
    });

    describe("Reordering rule tiers", () => {
        describe("Moving the top rule tier up", () => {
            test("should do nothing", done => {
                let entity = findRuleById(44);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(44);

                setDialogState(dialogStates.entityTypes.edit, dialogStates.entityTypes.tieredRateRule, entity);

                let child = entity.tiers[0];
                expect(child).toBeDefined();
                expect(child.id).toBe(3);

                let parent = findParentRuleset(44);
                expect(parent).toBeDefined();

                let updaterInvoked = false;

                function recordInvocation(swapPrimary, updatedEntity) {
                    updaterInvoked = true;
                }

                moveRuleTierUp(true, child, recordInvocation, done);
                expect(updaterInvoked).toBe(false);
                done();
            });
        });

        describe("Moving a rule tier up", () => {
            test("should swap the ordinal of the selected tier and the previous tier and then refresh the tier display", done => {
                let entity = findRuleById(44);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(44);

                setDialogState(dialogStates.entityTypes.edit, dialogStates.entityTypes.tieredRateRule, entity);

                let child = entity.tiers[2];
                expect(child).toBeDefined();
                expect(child.id).toBe(5);

                let parent = findParentRuleset(44);
                expect(parent).toBeDefined();

                let selectedEntityChecked = false;
                let previousEntityChecked = false

                function checkOrdinal(swapPrimary, updatedEntity) {
                    if (updatedEntity.id == 5) {
                        expect(updatedEntity.ordinal).toBe(2);
                        selectedEntityChecked = true;
                    } else if (updatedEntity.id == 4) {
                        expect(updatedEntity.ordinal).toBe(3);
                        previousEntityChecked = true;
                    }
                }

                moveRuleTierUp(true, child, checkOrdinal, done);
                expect(selectedEntityChecked && previousEntityChecked).toBe(true);
            });
        });

        describe("Moving a rule tier down", () => {
            test("should swap the ordinal of the selected tier and the next tier and then refresh the tiers display", done => {
                let entity = findRuleById(44);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(44);

                setDialogState(dialogStates.entityTypes.edit, dialogStates.entityTypes.tieredRateRule, entity);

                let child = entity.tiers[2];
                expect(child).toBeDefined();
                expect(child.id).toBe(5);

                let parent = findParentRuleset(44);
                expect(parent).toBeDefined();

                let selectedEntityChecked = false;
                let nextEntityChecked = false

                function checkOrdinal(swapPrimary, updatedEntity) {
                    if (updatedEntity.id == 5) {
                        expect(updatedEntity.ordinal).toBe(4);
                        selectedEntityChecked = true;
                    } else if (updatedEntity.id == 6) {
                        expect(updatedEntity.ordinal).toBe(3);
                        nextEntityChecked = true;
                    }
                }

                moveRuleTierDown(true, child, checkOrdinal, done);
                expect(selectedEntityChecked && nextEntityChecked).toBe(true);
            });
        });

        describe("Moving the bottom rule tier down", () => {
            test("should do nothing", done => {
                let entity = findRuleById(44);
                expect(entity).toBeDefined();
                expect(entity.id).toBe(44);

                setDialogState(dialogStates.entityTypes.edit, dialogStates.entityTypes.tieredRateRule, entity);

                let child = entity.tiers[3];
                expect(child).toBeDefined();
                expect(child.id).toBe(6);

                let updaterInvoked = false;

                function recordInvocation(swapPrimary, updatedEntity) {
                    updaterInvoked = true;
                }

                moveRuleTierDown(true, child, recordInvocation, done);
                expect(updaterInvoked).toBe(false);
                done();
            });
        });
    });
});