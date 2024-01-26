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
const { showDialog, hideDialog } = require("../view_utils.js");

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
});

describe("Multilple choice option views", () => {
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
});

describe("Ruleset views", () => {
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
});

describe("Rule views views", () => {
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
});

describe("Rule tier views views", () => {

});