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
    app, findQuestionById, findRuleById, getRulesByTypeForJurisdiction
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
        describe("Show and hide dialog", () => {
            test("should correctly display then hide status dialog", () => {
                let dialogId = statusDialog.dialog.id;
                showDialog(dialogId);
                expect(isShown(dialogId)).toBe(true);
                hideDialog(dialogId);
                expect(isShown(dialogId)).toBe(false);
            });
        });
    });

    describe("Status dialogs", () => {
        describe("Error dialog", () => {
            test("should correctly display an error dialog with the correct title and message", () => {
                let dialogConsts = statusDialog;
                let dialogId = dialogConsts.dialog.id;
                let title = "An Error Occurred";
                let message = "A test error";
                error(message);
                expect(isShown(dialogId)).toBe(true);
                let dialogLabel = document.getElementById(dialogConsts.label.id).innerHTML;
                expect(dialogLabel).toBe(title);

                let dialogMessage = document.getElementById(dialogConsts.message.id).innerHTML;
                expect(dialogMessage).toBe(message);
            });
        });

        describe("Success dialog", () => {
            test("should correctly display a success dialog with the correct title and message", () => {
                let dialogConsts = statusDialog;
                let dialogId = dialogConsts.dialog.id;
                let title = "Success";
                let message = "A test success message";
                success(message);
                expect(isShown(dialogId)).toBe(true);
                let dialogLabel = document.getElementById(dialogConsts.label.id).innerHTML;
                expect(dialogLabel).toBe(title);

                let dialogMessage = document.getElementById(dialogConsts.message.id).innerHTML;
                expect(dialogMessage).toBe(message);
            });
        });

        describe("Confirmation dialog", () => {
            test("should correctly display a confirmation dialog with the correct title and message", () => {
                let dialogConsts = confirmationDialog;
                let dialogId = dialogConsts.dialog.id;
                let title = "Are you sure?";
                let message = "A test confirmation message";
                confirm(message, function() {});
                expect(isShown(dialogId)).toBe(true);
                let dialogLabel = document.getElementById(dialogConsts.label.id).innerHTML;
                expect(dialogLabel).toBe(title);

                let dialogMessage = document.getElementById(dialogConsts.message.id).innerHTML;
                expect(dialogMessage).toBe(message);
            });
        });
    });

    describe("Question dialogs", () => {
        describe("Boolean question dialog", () => {
            describe("Create", () => {
                test("should correctly display the create boolean question dialog", () => {
                    let dialogConsts = booleanQuestionDialog;
                    displayCreateBooleanQuestionDialog();
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let text = document.getElementById(dialogConsts.questionText.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let isMandatory = document.getElementById(dialogConsts.isMandatory.input.id).checked;

                    expect(text).toBe("");
                    expect(explainer).toBe("");
                    expect(variableName).toBe("");
                    expect(isMandatory).toBe(false);
                });
            });

            describe("Edit", () => {
                test("should correctly display the edit boolean question dialog for the given question", () => {
                    let question = findQuestionById(3);
                    expect(question).toBeDefined();
                    expect(question.id).toBe(3);

                    let dialogConsts = booleanQuestionDialog;
                    displayEditBooleanQuestionDialog(question);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let text = document.getElementById(dialogConsts.questionText.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let isMandatory = document.getElementById(dialogConsts.isMandatory.input.id).checked;

                    expect(text).toBe(question.text);
                    expect(explainer).toBe(question.explainer);
                    expect(variableName).toBe(question.variable_name);
                    expect(isMandatory).toBe(question.is_mandatory);
                });
            });
        });

        describe("Numeric question dialog", () => {
            describe("Create", () => {
                test("should correctly display the create numeric question dialog", () => {
                    let dialogConsts = numericQuestionDialog;
                    displayCreateNumericQuestionDialog();
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let text = document.getElementById(dialogConsts.questionText.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let isMandatory = document.getElementById(dialogConsts.isMandatory.input.id).checked;
                    let isInteger = document.getElementById(dialogConsts.isInteger.input.id).checked;
                    let minValue = document.getElementById(dialogConsts.minimumValue.input.id).value;
                    let maxValue = document.getElementById(dialogConsts.maximumValue.input.id).value;

                    expect(text).toBe("");
                    expect(explainer).toBe("");
                    expect(variableName).toBe("");
                    expect(isMandatory).toBe(false);
                    expect(isInteger).toBe(false);
                    expect(minValue).toBe("");
                    expect(maxValue).toBe("");
                });
            });

            describe("Edit", () => {
                test("should correctly display the edit numeric question dialog for the given question", () => {
                    let question = findQuestionById(4);
                    expect(question).toBeDefined();
                    expect(question.id).toBe(4);

                    let dialogConsts = numericQuestionDialog;
                    displayEditNumericQuestionDialog(question);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let text = document.getElementById(dialogConsts.questionText.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let isMandatory = document.getElementById(dialogConsts.isMandatory.input.id).checked;
                    let isInteger = document.getElementById(dialogConsts.isInteger.input.id).checked;
                    let minValue = document.getElementById(dialogConsts.minimumValue.input.id).value;
                    let maxValue = document.getElementById(dialogConsts.maximumValue.input.id).value;

                    expect(text).toBe(question.text);
                    expect(explainer).toBe(question.explainer);
                    expect(variableName).toBe(question.variable_name);
                    expect(isMandatory).toBe(question.is_mandatory);
                    expect(isInteger).toBe(question.is_integer);
                    expect(parseInt(minValue)).toBe(question.min_value);
                    expect(parseInt(maxValue)).toBe(question.max_value);
                });
            });
        });

        describe("Multiple choice question dialog", () => {
            describe("Create", () => {
                test("should correctly display the create multiple choice question dialog", () => {
                    let dialogConsts = multipleChoiceQuestionDialog;
                    displayCreateMultipleChoiceQuestionDialog();
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let text = document.getElementById(dialogConsts.questionText.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let isMandatory = document.getElementById(dialogConsts.isMandatory.input.id).checked;
                    let allowMultiselect = document.getElementById(dialogConsts.allowMultiselect.input.id).checked;

                    expect(text).toBe("");
                    expect(explainer).toBe("");
                    expect(variableName).toBe("");
                    expect(isMandatory).toBe(false);
                    expect(allowMultiselect).toBe(false);

                    let optionTable = document.getElementById(dialogConsts.options.table.id);
                    expect(optionTable).toBeDefined();
                    expect(optionTable.children.length).toBe(1);
                });
            });

            describe("Edit", () => {
                test("should correctly display the edit multiple choice question dialog for the given question", () => {
                    let question = findQuestionById(7);
                    expect(question).toBeDefined();
                    expect(question.id).toBe(7);

                    let dialogConsts = multipleChoiceQuestionDialog;
                    displayEditMultipleChoiceQuestionDialog(question);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let text = document.getElementById(dialogConsts.questionText.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let isMandatory = document.getElementById(dialogConsts.isMandatory.input.id).checked;
                    let allowMultiselect = document.getElementById(dialogConsts.allowMultiselect.input.id).checked;

                    expect(text).toBe(question.text);
                    expect(explainer).toBe(question.explainer);
                    expect(variableName).toBe(question.variable_name);
                    expect(isMandatory).toBe(question.is_mandatory);

                    let optionTable = document.getElementById(dialogConsts.options.table.id);
                    expect(optionTable).toBeDefined();
                    expect(optionTable.children.length).toBe(question.options.length + 1);
                });
            });
        });
    });

    describe("Multiple choice option dialog", () => {
        describe("Create", () => {
            test("should correctly display the create multiple choice option dialog", () => {
                let dialogConsts = multipleChoiceOptionDialog;
                displayCreateMultipleChoiceOptionDialog();
                expect(isShown(dialogConsts.dialog.id)).toBe(true);
                
                let name = document.getElementById(dialogConsts.name.input.id).value;
                let explainer = document.getElementById(dialogConsts.explainer.input.id).value;

                expect(name).toBe("");
                expect(explainer).toBe("");
            });
        });
    });

    describe("Ruleset dialog", () => {
        describe("Create", () => {
            test("should correctly display the create ruleset dialog", () => {
                let dialogConsts = rulesetDialog;
                displayCreateRulesetDialog()
                expect(isShown(dialogConsts.dialog.id)).toBe(true);
                
                let taxCategories = document.getElementById(dialogConsts.taxCategory.input.id);
                expect(taxCategories.selectedIndex).toBe(0);
                expect(taxCategories.children.length).toBe(app.taxCategories.length);
                
                for (var i = 0; i < taxCategories.children.length; i++) {
                    expect(parseInt(taxCategories.children[i].value)).toBe(app.taxCategories[i].tax_category_id);
                }
            });
        });
    });

    describe("Rule dialogs", () => {
        describe("Flat rate rule dialog", () => {
            describe("Create", () => {
                test("should correctly display the create flat rate rule dialog", () => {
                    let dialogConsts = flatRateRuleDialog;
                    displayCreateFlatRateRuleDialog();
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let name = document.getElementById(dialogConsts.name.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let taxRate = document.getElementById(dialogConsts.taxRate.input.id).value;

                    expect(name).toBe("");
                    expect(explainer).toBe("");
                    expect(variableName).toBe("");
                    expect(taxRate).toBe("");
                });
            });

            describe("Edit", () => {
                test("should correctly display the edit flat rate rule dialog", () => {
                    let rule = findRuleById(19);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(19);
                    expect(rule.type).toBe("flat_rate");

                    let dialogConsts = flatRateRuleDialog;
                    displayEditFlatRateRuleDialog(rule);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let name = document.getElementById(dialogConsts.name.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let taxRate = document.getElementById(dialogConsts.taxRate.input.id).value;

                    expect(name).toBe(rule.name);
                    expect(explainer).toBe(rule.explainer);
                    expect(variableName).toBe(rule.variable_name);
                    expect(parseInt(taxRate)).toBe(rule.tax_rate);
                });
            });
        });

        describe("Tiered rate rule dialog", () => {
            describe("Create", () => {
                test("should correctly display the create tiered rate rule dialog", () => {
                    let dialogConsts = tieredRateRuleDialog;
                    displayCreateTieredRateRuleDialog();
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let name = document.getElementById(dialogConsts.name.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;

                    expect(name).toBe("");
                    expect(explainer).toBe("");
                    expect(variableName).toBe("");

                    let tiersTable = document.getElementById(dialogConsts.tiers.table.id);
                    expect(tiersTable).toBeDefined();
                    expect(tiersTable.children.length).toBe(1);
                });
            });

            describe("Edit", () => {
                test("should correctly display the create tiered rate rule dialog", () => {
                    let rule = findRuleById(44);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(44);
                    expect(rule.type).toBe("tiered_rate");

                    let dialogConsts = tieredRateRuleDialog;
                    displayEditTieredRateRuleDialog(rule);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let name = document.getElementById(dialogConsts.name.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;

                    expect(name).toBe(rule.name);
                    expect(explainer).toBe(rule.explainer);
                    expect(variableName).toBe(rule.variable_name);

                    let tiersTable = document.getElementById(dialogConsts.tiers.table.id);
                    expect(tiersTable).toBeDefined();
                    expect(tiersTable.children.length).toBe(rule.tiers.length + 1);
                });
            });
        });

        describe("Secondary tiered rate rule dialog", () => {
            describe("Create", () => {
                test("should correctly display the create secondary tiered rate rule dialog", () => {
                    let primaryRules = getRulesByTypeForJurisdiction("tiered_rate");
                    let dialogConsts = secondaryTieredRateRuleDialog;

                    displayCreateSecondaryTieredRateRuleDialog(primaryRules);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let name = document.getElementById(dialogConsts.name.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let primaryRuleSelect = document.getElementById(dialogConsts.primaryRule.input.id);

                    expect(name).toBe("");
                    expect(explainer).toBe("");
                    expect(variableName).toBe("");
                    expect(primaryRuleSelect.children.length).toBe(primaryRules.length);
                    for (var i = 0; i < primaryRuleSelect.children.length; i++) {
                        expect(parseInt(primaryRuleSelect.children[i].value)).toBe(primaryRules[i].id);
                    }

                    let tiersTable = document.getElementById(dialogConsts.tiers.table.id);
                    expect(tiersTable).toBeDefined();
                    expect(tiersTable.children.length).toBe(1);
                });
            });

            describe("Edit", () => {
                test("should correctly display the create secondary tiered rate rule dialog", () => {
                    let rule = findRuleById(45);
                    expect(rule).toBeDefined();
                    expect(rule.id).toBe(45);
                    expect(rule.type).toBe("secondary_tiered_rate");

                    let primaryRules = getRulesByTypeForJurisdiction("tiered_rate");
                    let dialogConsts = secondaryTieredRateRuleDialog;

                    displayEditSecondaryTieredRateRuleDialog(rule, primaryRules);
                    expect(isShown(dialogConsts.dialog.id)).toBe(true);
                    
                    let name = document.getElementById(dialogConsts.name.input.id).value;
                    let explainer = document.getElementById(dialogConsts.explainer.input.id).value;
                    let variableName = document.getElementById(dialogConsts.variableName.input.id).value;
                    let primaryRuleSelect = document.getElementById(dialogConsts.primaryRule.input.id);

                    expect(name).toBe(rule.name);
                    expect(explainer).toBe(rule.explainer);
                    expect(variableName).toBe(rule.variable_name);
                    expect(primaryRuleSelect.children.length).toBe(primaryRules.length);
                    for (var i = 0; i < primaryRuleSelect.children.length; i++) {
                        expect(parseInt(primaryRuleSelect.children[i].value)).toBe(primaryRules[i].id);
                    }

                    let tiersTable = document.getElementById(dialogConsts.tiers.table.id);
                    expect(tiersTable).toBeDefined();
                    expect(tiersTable.children.length).toBe(rule.tiers.length + 1);
                });
            });
        });
    });

    describe("Primary rule tier dialogs", () => {
        describe("Create", () => {
            test("should correctly display the create rule tier dialog", () => {
                let dialogConsts = ruleTierDialog;

                displayCreateRuleTierDialog();
                expect(isShown(dialogConsts.dialog.id)).toBe(true);

                let minValue = document.getElementById(dialogConsts.minimumValue.input.id).value;
                let maxValue = document.getElementById(dialogConsts.maximumValue.input.id).value;
                let taxRate = document.getElementById(dialogConsts.taxRate.input.id).value;

                expect(minValue).toBe("");
                expect(maxValue).toBe("");
                expect(taxRate).toBe("");
            });
        });

        describe("Edit", () => {
            test("should correctly display the edit rule tier dialog for the selected rule tier", () => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.type).toBe("tiered_rate");

                let tier = rule.tiers[0];

                let dialogConsts = ruleTierDialog;

                displayEditRuleTierDialog(tier);
                expect(isShown(dialogConsts.dialog.id)).toBe(true);

                let minValue = document.getElementById(dialogConsts.minimumValue.input.id).value;
                let maxValue = document.getElementById(dialogConsts.maximumValue.input.id).value;
                let taxRate = document.getElementById(dialogConsts.taxRate.input.id).value;

                expect(parseInt(minValue)).toBe(tier.min_value);
                expect(parseInt(maxValue)).toBe(tier.max_value);
                expect(parseInt(taxRate)).toBe(tier.tier_rate);
            });
        });
    });

    describe("Secondary rule tier dialogs", () => {
        describe("Create", () => {
            test("should correctly display the create secondary rule tier dialog", () => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.type).toBe("tiered_rate");
                expect(rule.tiers.length).toBe(4);

                let dialogConsts = secondaryRuleTierDialog;

                displayCreateSecondaryRuleTierDialog(rule.tiers);
                expect(isShown(dialogConsts.dialog.id)).toBe(true);

                let taxRate = document.getElementById(dialogConsts.taxRate.input.id).value;
                expect(taxRate).toBe("");

                let primaryTierSelect = document.getElementById(dialogConsts.primaryTier.input.id);
                expect(primaryTierSelect).toBeDefined();
                expect(primaryTierSelect.children).toBeDefined();
                expect(primaryTierSelect.children.length).toBe(rule.tiers.length);
                for (var i = 0; i < primaryTierSelect.children.length; i++) {
                    expect(parseInt(primaryTierSelect.children[i].value)).toBe(rule.tiers[i].id)
                }
            });
        });

        describe("Edit", () => {
            test("should correctly display the create secondary rule tier dialog", () => {
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.type).toBe("tiered_rate");
                expect(rule.tiers.length).toBe(4);

                let secondaryRule = findRuleById(45);
                expect(secondaryRule).toBeDefined();
                expect(secondaryRule.id).toBe(45);
                expect(secondaryRule.type).toBe("secondary_tiered_rate");
                expect(secondaryRule.tiers.length).toBe(1);

                let tier = secondaryRule.tiers[0];

                let dialogConsts = secondaryRuleTierDialog;

                displayEditSecondaryRuleTierDialog(tier, rule.tiers);
                expect(isShown(dialogConsts.dialog.id)).toBe(true);

                let taxRate = document.getElementById(dialogConsts.taxRate.input.id).value;
                expect(parseInt(taxRate)).toBe(tier.tier_rate);

                let primaryTierSelect = document.getElementById(dialogConsts.primaryTier.input.id);
                expect(primaryTierSelect).toBeDefined();
                expect(primaryTierSelect.children).toBeDefined();
                expect(primaryTierSelect.children.length).toBe(rule.tiers.length);
                for (var i = 0; i < primaryTierSelect.children.length; i++) {
                    expect(parseInt(primaryTierSelect.children[i].value)).toBe(rule.tiers[i].id)
                }
            });
        });
    });
});

describe("Select utilities", () => {
    describe("Jurisdictions select", () => {
        describe("Initialisation", () => {
            test("should correctly initialise the jurisdictions select box", () => {
                let select = document.getElementById(jurisdictionsSelect.id);
                expect(select).toBeDefined();
                expect(select.children).toBeDefined();

                initJurisdictionsSelect(app.jurisdictions, function () {});
                
                expect(select.children.length).toBe(app.jurisdictions.length);
                for (var i = 0; i < app.jurisdictions.length; i++) {
                    let selectNode = select.children[i];
                    let jurisdiction = app.jurisdictions[i];
                    expect(parseInt(selectNode.value)).toBe(jurisdiction.id);
                    expect(selectNode.text).toBe(jurisdiction.name);
                }
            });
        });
    });

    describe("Primary rule select", () => {
        describe("Initialisation", () => {
            test("should correctly initialise the primary rule select box", () => {
                let select = document.getElementById(secondaryTieredRateRuleDialog.primaryRule.input.id);
                expect(select).toBeDefined();
                expect(select.children).toBeDefined();

                let rules = getRulesByTypeForJurisdiction("tiered_rate");
                expect(rules).toBeDefined();
                expect(rules.length).toBe(2);

                initPrimaryRulesSelect(rules);
                
                expect(select.children.length).toBe(rules.length);
                for (var i = 0; i < rules.length; i++) {
                    let selectNode = select.children[i];
                    let rule = rules[i];
                    expect(parseInt(selectNode.value)).toBe(rule.id);
                    expect(selectNode.text).toBe(rule.name);
                }
            });
        });
    });

    describe("Primary rule tiers select", () => {
        describe("Initialisation", () => {
            test("should correctly initialise the primary rule select box", () => {
                let select = document.getElementById(secondaryRuleTierDialog.primaryTier.input.id);
                expect(select).toBeDefined();
                expect(select.children).toBeDefined();

                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.tiers.length).toBe(4);

                initPrimaryRuleTiersSelect(rule.tiers);
                
                expect(select.children.length).toBe(rule.tiers.length);
                for (var i = 0; i < rule.tiers.length; i++) {
                    let selectNode = select.children[i];
                    let tier = rule.tiers[i];
                    expect(parseInt(selectNode.value)).toBe(tier.id);
                    expect(selectNode.text).toBe(tier.min_value + " - " + tier.max_value + " (" + tier.tier_rate + ")");
                }
            });
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