const { dialogStates } = require("../view_consts");
const { buildAppState } = require("./mocks/view_models.mocks.js");
const {
    app,
    clearDialogState,
    setDialogState,
    setParentState,
    clearParentState,
    moveAppStateToParentState,
    moveParentStateToAppState,
    setParentRuleset,
    getForm,
    getFormId,
    getTaxCategoryById,
    getQuestions,
    getNextQuestionOrdinal,
    findQuestionById,
    getTieredRateRulesForJurisdiction,
    findRuleById,
    findParentRuleset,
    findPrimaryRuleTierById,
    findPreviousQuestion,
    findNextQuestion,
    resequenceQuestionOrdinals,
    getNextRulesetOrdinal,
    findPreviousRuleset,
    findNextRuleset,
    resequenceRulesetOrdinals,
    getRulesByTypeForJurisdiction,
    getNextRuleOrdinal,
    findPreviousRule,
    findNextRule,
    resequenceRuleOrdinals,
    getNextRuleTierOrdinal,
    findPreviousRuleTier,
    findNextRuleTier,
    resequenceRuleTierOrdinals
 } = require("../view_models");

describe("App state management", () => {
    describe("Dialog state management", () => {
        test("should correctly set then clear the dialog state", () => {
            setDialogState(dialogStates.modes.create, dialogStates.entityTypes.booleanQuestion, { test: "test" });
            expect(app.dialogState.mode).toBe(dialogStates.modes.create);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.booleanQuestion);
            expect(app.dialogState.entity).toBeDefined();
            expect(app.dialogState.entity.test).toBe("test");

            clearDialogState();
            expect(app.dialogState.mode).toBeNull();
            expect(app.dialogState.entityType).toBeNull();
            expect(app.dialogState.entity).toBeNull();
        });
    });

    describe("Parent state management", () => {
        test("should correctly set then clear the parent state", () => {
            setParentState(dialogStates.modes.create, dialogStates.entityTypes.booleanQuestion, { test: "test" });
            expect(app.parentState.mode).toBe(dialogStates.modes.create);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.booleanQuestion);
            expect(app.parentState.entity).toBeDefined();
            expect(app.parentState.entity.test).toBe("test");

            clearParentState();
            expect(app.parentState.mode).toBeNull();
            expect(app.parentState.entityType).toBeNull();
            expect(app.parentState.entity).toBeNull();
        });

        test("should correctly move the app state to the parent state and then back", () => {
            // Set up the dialog state and test it
            setDialogState(dialogStates.modes.create, dialogStates.entityTypes.booleanQuestion, { test: "test" });
            expect(app.dialogState.mode).toBe(dialogStates.modes.create);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.booleanQuestion);
            expect(app.dialogState.entity).toBeDefined();
            expect(app.dialogState.entity.test).toBe("test");

            // Move it to the parent state and then re-check
            moveAppStateToParentState();
            expect(app.parentState.mode).toBe(dialogStates.modes.create);
            expect(app.parentState.entityType).toBe(dialogStates.entityTypes.booleanQuestion);
            expect(app.parentState.entity).toBeDefined();
            expect(app.parentState.entity.test).toBe("test");

            // Move it back and perform final checks
            moveParentStateToAppState();
            expect(app.dialogState.mode).toBe(dialogStates.modes.create);
            expect(app.dialogState.entityType).toBe(dialogStates.entityTypes.booleanQuestion);
            expect(app.dialogState.entity).toBeDefined();
            expect(app.dialogState.entity.test).toBe("test");
        });

        test("should correctly set the parent ruleset in the app state", () => {
            setParentRuleset({ "id": 1, "jurisdiction_id": 1, "tax_category_id": 1 });
            expect(app.parentRuleset).toBeDefined();
            expect(app.parentRuleset.id).toBe(1);
            expect(app.parentRuleset.jurisdiction_id).toBe(1);
            expect(app.parentRuleset.tax_category_id).toBe(1);
        });
    });
});

beforeEach(() => {
    appState = buildAppState();
    app.jurisdictions = appState.jurisdictions;
    app.taxCategories = appState.taxCategories;
    app.jurisdictionForm = appState.jurisdictionForm;
    app.jurisdictionRules = appState.jurisdictionRules;
});

describe("View model accessor methods", () => {
    describe("Forms", () => {
        test("should return the correct form from view model", () => {
            let form = getForm();
            expect(form).toBeDefined();
            expect(form.id).toBe(1);
            expect(form.jurisdiction_id).toBe(1);
            expect(form.questions).toBeDefined();
            expect(form.questions.length).toBe(3);
        });

        test("should return the correct form id from view model", () => {
            let formId = getFormId();
            expect(formId).toBe(1);
        });
    });

    describe("Tax categories", () => {
        test("should return the correct tax category for a valid id", () => {
            let taxCategory = getTaxCategoryById(1);
            expect(taxCategory).toBeDefined();
            expect(taxCategory.tax_category_id).toBe(1);
            expect(taxCategory.name).toBe("Dividend Tax");
        });

        test("should return null for an invalid id", () => {
            let taxCategory = getTaxCategoryById(42);
            expect(taxCategory).toBeNull();
        });
    });

    describe("Questions", () => {
        test("should return the correct list of questions", () => {
            let questions = getQuestions();
            expect(questions.length).toBe(3);
            
            expect(questions[0].id).toBe(3);
            expect(questions[0].type).toBe("boolean");
            expect(questions[0].ordinal).toBe(1);

            expect(questions[1].id).toBe(4);
            expect(questions[1].type).toBe("numeric");
            expect(questions[1].ordinal).toBe(2);

            expect(questions[2].id).toBe(7);
            expect(questions[2].type).toBe("multiple_choice");
            expect(questions[2].ordinal).toBe(3);
        });

        test("should return the correct question given a valid id", () => {
            let question = findQuestionById(3);
            expect(question.id).toBe(3);
            expect(question.text).toBe("A boolean question test");
            expect(question.type).toBe("boolean");
            expect(question.ordinal).toBe(1);
        });

        test("should return null given an invalid id", () => {
            let question = findQuestionById(42);
            expect(question).toBeNull();
        });
    });

    describe("Rulesets", () => {
        test("return a valid ruleset given a valid rule id", () => {
            let ruleset = findParentRuleset(13);
            expect(ruleset).toBeDefined();
            expect(ruleset.id).toBe(23);
            expect(ruleset.tax_category_id).toBe(1);
        });

        test("return null given an invalid rule id", () => {
            let ruleset = findParentRuleset(42);
            expect(ruleset).toBeNull();
        });
    });

    describe("Rules", () => {
        test("return a valid rule given a valid rule id", () => {
            let rule = findRuleById(13);
            expect(rule).toBeDefined();
            expect(rule.id).toBe(13);
            expect(rule.ordinal).toBe(1);
            expect(rule.name).toBe("Income Tax Bands");
            expect(rule.type).toBe("tiered_rate");
        });

        test("return null given an invalid rule id", () => {
            let rule = findRuleById(42);
            expect(rule).toBeNull();
        });

        test("return all tiered rate rules for the current jurisdiction contained in the app state", () => {
            let tieredRules = getTieredRateRulesForJurisdiction();
            expect(tieredRules).toBeDefined();
            expect(tieredRules.length).toBe(2);

            expect(tieredRules[0].id).toBe(13);
            expect(tieredRules[0].ordinal).toBe(1);
            expect(tieredRules[0].name).toBe("Income Tax Bands");
            expect(tieredRules[0].type).toBe("tiered_rate");

            expect(tieredRules[1].id).toBe(44);
            expect(tieredRules[1].ordinal).toBe(2);
            expect(tieredRules[1].name).toBe("Rule 2");
            expect(tieredRules[1].type).toBe("tiered_rate");
        });

        test("return all flat rate rules for the current jurisdiction", () => {
            let rules = getRulesByTypeForJurisdiction("flat_rate");
            expect(rules).toBeDefined();
            expect(rules.length).toBe(2);

            expect(rules[0].id).toBe(19);
            expect(rules[0].ordinal).toBe(1);
            expect(rules[0].name).toBe("Corporation Tax");
            expect(rules[0].type).toBe("flat_rate");

            expect(rules[1].id).toBe(41);
            expect(rules[1].ordinal).toBe(1);
            expect(rules[1].name).toBe("Rule 1");
            expect(rules[1].type).toBe("flat_rate");
        });

        test("return all tiered rate rules for the current jurisdiction", () => {
            let rules = getRulesByTypeForJurisdiction("tiered_rate");
            expect(rules).toBeDefined();
            expect(rules.length).toBe(2);

            expect(rules[0].id).toBe(13);
            expect(rules[0].ordinal).toBe(1);
            expect(rules[0].name).toBe("Income Tax Bands");
            expect(rules[0].type).toBe("tiered_rate");

            expect(rules[1].id).toBe(44);
            expect(rules[1].ordinal).toBe(2);
            expect(rules[1].name).toBe("Rule 2");
            expect(rules[1].type).toBe("tiered_rate");
        });

        test("return all secondary tiered rate rules for the current jurisdiction", () => {
            let rules = getRulesByTypeForJurisdiction("secondary_tiered_rate");
            expect(rules).toBeDefined();
            expect(rules.length).toBe(2);

            expect(rules[0].id).toBe(15);
            expect(rules[0].ordinal).toBe(1);
            expect(rules[0].name).toBe("Dividend Tax Bands");
            expect(rules[0].type).toBe("secondary_tiered_rate");

            expect(rules[1].id).toBe(45);
            expect(rules[1].ordinal).toBe(3);
            expect(rules[1].name).toBe("Rule 3");
            expect(rules[1].type).toBe("secondary_tiered_rate");
        });

        test("return empty array given an invalid rule type", () => {
            let rules = getRulesByTypeForJurisdiction("nonsense");
            expect(rules).toBeDefined();
            expect(rules.length).toBe(0);
        });
    });

    describe("Rule tiers", () => {
        test("return correct primary rule tier given a valid id", () => {
            let tier = findPrimaryRuleTierById(3);
            expect(tier).toBeDefined();
            expect(tier.id).toBe(3);
            expect(tier.min_value).toBe(0);
            expect(tier.max_value).toBe(15000);
            expect(tier.ordinal).toBe(1);
            expect(tier.tier_rate).toBe(12.0);
        });

        test("return null given an invalid rule tier id", () => {
            let tier = findPrimaryRuleTierById(42);
            expect(tier).toBeNull();
        });
    });
});

describe("Ordinal traversal and management", () => {
    describe("Question ordinals", () => {
        describe("Get next ordinal", () => {
            test("should return the correct ordinal given the mock app state", () => {
                let nextOrdinal = getNextQuestionOrdinal();
                expect(nextOrdinal).toBeDefined();
                expect(nextOrdinal).toBe(4);
            });
            
        });

        describe("Find previous", () => {
            test("should return the correct question given a valid question", () => {
                // Retrieve and check the question
                let question = findQuestionById(4);
                expect(question).toBeDefined();
                expect(question.id).toBe(4);
                expect(question.ordinal).toBe(2);

                // Retrieve and check the next question by ordinal
                let previousQuestion = findPreviousQuestion(question);
                expect(previousQuestion).toBeDefined();
                expect(previousQuestion.id).toBe(3);
                expect(previousQuestion.ordinal).toBe(1);
            });

            test("should return null given null input", () => {
                let previousQuestion = findPreviousQuestion(null);
                expect(previousQuestion).toBeNull();
            });

            test("should return null given undefined input", () => {
                let previousQuestion = findPreviousQuestion(undefined);
                expect(previousQuestion).toBeNull();
            });

            test("should return null given an invalid object", () => {
                let previousQuestion = findPreviousQuestion({});
                expect(previousQuestion).toBeNull();
            });
        });

        describe("Find next", () => {
            test("should return the correct question given a valid question", () => {
                // Retrieve and check the question
                let question = findQuestionById(4);
                expect(question).toBeDefined();
                expect(question.id).toBe(4);
                expect(question.ordinal).toBe(2);

                // Retrieve and check the next question by ordinal
                let nextQuestion = findNextQuestion(question);
                expect(nextQuestion).toBeDefined();
                expect(nextQuestion.id).toBe(7);
                expect(nextQuestion.ordinal).toBe(3);
            });

            test("should return null given null input", () => {
                let nextQuestion = findNextQuestion(null);
                expect(nextQuestion).toBeNull();
            });

            test("should return null given undefined input", () => {
                let nextQuestion = findNextQuestion(undefined);
                expect(nextQuestion).toBeNull();
            });

            test("should return null given an invalid object", () => {
                let nextQuestion = findNextQuestion({});
                expect(nextQuestion).toBeNull();
            });
        });

        describe("Resequence ordinals", () => {
            test("should ensure that ordinals are sequential, starting with 1, after middle question is deleted", () => {
                let i = 1;

                // Get the question we are going to delete
                let deletedQuestion = app.jurisdictionForm.forms["1"].questions[i];

                // Now delete the question from the list
                expect(app.jurisdictionForm.forms["1"].questions.length).toBe(3);
                app.jurisdictionForm.forms["1"].questions.splice(i, 1);
                expect(app.jurisdictionForm.forms["1"].questions.length).toBe(2);

                // Now resequence the ordinals
                let questions = resequenceQuestionOrdinals(deletedQuestion);
                expect(questions[0].id).toBe(3);
                expect(questions[0].ordinal).toBe(1);

                expect(questions[1].id).toBe(7);
                expect(questions[1].ordinal).toBe(2);
            });
        });
    });

    describe("Ruleset ordinals", () => {
        describe("Get next ordinal", () => {
            test("should return the correct ordinal given the mock app state", () => {
                let nextOrdinal = getNextRulesetOrdinal();
                expect(nextOrdinal).toBeDefined();
                expect(nextOrdinal).toBe(5);
            });
        });

        describe("Find previous", () => {
            test("should return the correct ruleset given a valid ruleset", () => {
                // Retrieve and check the question
                let ruleset = findParentRuleset(19);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(26);
                expect(ruleset.ordinal).toBe(3);

                // Retrieve and check the next question by ordinal
                let previousRuleset = findPreviousRuleset(ruleset);
                expect(previousRuleset).toBeDefined();
                expect(previousRuleset.id).toBe(24);
                expect(previousRuleset.ordinal).toBe(2);
            });

            test("should return null given null input", () => {
                let previousRuleset = findPreviousRuleset(null);
                expect(previousRuleset).toBeNull();
            });

            test("should return null given undefined input", () => {
                let previousRuleset = findPreviousRuleset(undefined);
                expect(previousRuleset).toBeNull();
            });

            test("should return null given an invalid object", () => {
                let previousRuleset = findPreviousRuleset({});
                expect(previousRuleset).toBeNull();
            });
        });

        describe("Find next", () => {
            test("should return the correct ruleset given a valid ruleset", () => {
                // Retrieve and check the question
                let ruleset = findParentRuleset(19);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(26);
                expect(ruleset.ordinal).toBe(3);
                // Retrieve and check the next question by
                let nextRuleset = findNextRuleset(ruleset);
                expect(nextRuleset).toBeDefined();
                expect(nextRuleset.id).toBe(27);
                expect(nextRuleset.ordinal).toBe(4);
            });

            test("should return null given null input", () => {
                let nextRuleset = findNextRuleset(null);
                expect(nextRuleset).toBeNull();
            });

            test("should return null given undefined input", () => {
                let nextRuleset = findNextRuleset(undefined);
                expect(nextRuleset).toBeNull();
            });

            test("should return null given an invalid object", () => {
                let nextRuleset = findNextRuleset({});
                expect(nextRuleset).toBeNull();
            });
        });

        describe("Resequence ordinals", () => {
            test("should ensure that ordinals are sequential, starting with 1, after middle ruleset is deleted", () => {
                let i = 2;

                // Get the ruleset we are going to delete
                let deletedRuleset = app.jurisdictionRules[i];

                // Now delete the ruleset from the list
                expect(app.jurisdictionRules.length).toBe(4);
                app.jurisdictionRules.splice(i, 1);
                expect(app.jurisdictionRules.length).toBe(3);

                // Now resequence the ordinals
                let rulesets = resequenceRulesetOrdinals(deletedRuleset);
                expect(rulesets[0].id).toBe(23);
                expect(rulesets[0].ordinal).toBe(1);

                expect(rulesets[1].id).toBe(24);
                expect(rulesets[1].ordinal).toBe(2);

                expect(rulesets[2].id).toBe(27);
                expect(rulesets[2].ordinal).toBe(3);
            });
        });
    });

    describe("Rule ordinals", () => {
        describe("Get next ordinal", () => {
            test("should return the correct ordinal given the mock app state", () => {
                // Set up the parent ruleset
                let parentRuleset = findParentRuleset(41);
                expect(parentRuleset).toBeDefined();
                expect(parentRuleset.id).toBe(27);
                setParentRuleset(parentRuleset);

                // Check that we retrieve the right next ordinal
                let nextOrdinal = getNextRuleOrdinal();
                expect(nextOrdinal).toBeDefined();
                expect(nextOrdinal).toBe(4);
            });
        });

        describe("Find previous", () => {
            test("should return the correct rule given a valid rule", () => {
                // Retrieve and check the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);

                // Get parent ruleset
                let ruleset = findParentRuleset(rule.id);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                // Retrieve and check the next rule by ordinal
                let previousRule = findPreviousRule(ruleset, rule);
                expect(previousRule).toBeDefined();
                expect(previousRule.id).toBe(41);
                expect(previousRule.ordinal).toBe(1);
            });

            test("should return null given null input", () => {
                // Get parent ruleset
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                let previousRule = findPreviousRule(ruleset, null);
                expect(previousRule).toBeNull();
            });

            test("should return null given undefined input", () => {
                // Get parent ruleset
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                let previousRule = findPreviousRule(ruleset, undefined);
                expect(previousRule).toBeNull();
            });

            test("should return null given an invalid object", () => {
                // Get parent ruleset
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                let previousRule = findPreviousRule(ruleset, {});
                expect(previousRule).toBeNull();
            });
        });

        describe("Find next", () => {
            test("should return the correct rule given a valid rule", () => {
                // Retrieve and check the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);

                // Get parent ruleset
                let ruleset = findParentRuleset(rule.id);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                // Retrieve and check the next rule by ordinal
                let nextRule = findNextRule(ruleset, rule);
                expect(nextRule).toBeDefined();
                expect(nextRule.id).toBe(45);
                expect(nextRule.ordinal).toBe(3);
            });

            test("should return null given null input", () => {
                // Get parent ruleset
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                let nextRule = findNextRule(ruleset, null);
                expect(nextRule).toBeNull();
            });

            test("should return null given undefined input", () => {
                // Get parent ruleset
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                let nextRule = findNextRule(ruleset, undefined);
                expect(nextRule).toBeNull();
            });

            test("should return null given an invalid object", () => {
                // Get parent ruleset
                let ruleset = findParentRuleset(44);
                expect(ruleset).toBeDefined();
                expect(ruleset.id).toBe(27);
                expect(ruleset.ordinal).toBe(4);

                let nextRule = findNextRule(ruleset, {});
                expect(nextRule).toBeNull();
            });
        });

        describe("Resequence ordinals", () => {
            test("should ensure that ordinals are sequential, starting with 1, after middle rule is deleted", () => {
                let rulesetI = 3;
                let ruleI = 1;

                setParentRuleset(app.jurisdictionRules[rulesetI]);
                // Get the ruleset we are going to delete
                let deletedRule = app.jurisdictionRules[rulesetI].rules[ruleI];

                expect(deletedRule.id).toBe(44);
                expect(deletedRule.ordinal).toBe(2);

                // Now delete the ruleset from the list
                expect(app.jurisdictionRules[rulesetI].rules.length).toBe(3);
                app.jurisdictionRules[rulesetI].rules.splice(ruleI, 1);
                expect(app.jurisdictionRules[rulesetI].rules.length).toBe(2);

                // Now resequence the ordinals
                let rules = resequenceRuleOrdinals(deletedRule);
                expect(rules[0].id).toBe(41);
                expect(rules[0].ordinal).toBe(1);

                expect(rules[1].id).toBe(45);
                expect(rules[1].ordinal).toBe(2);
            });
        });
    });

    describe("Rule tier ordinals", () => {
        describe("Get next ordinal", () => {
            test("should return the correct ordinal given the mock app state", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.tiers).toBeDefined();
                expect(rule.tiers.length).toBe(4);

                // Check we get the right ordinal
                let nextOrdinal = getNextRuleTierOrdinal(rule);
                expect(nextOrdinal).toBeDefined();
                expect(nextOrdinal).toBe(5);
            });
        });

        describe("Find previous", () => {
            test("should return the correct rule tier given a valid rule tier", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                // Retrieve and check the rule tier
                let ruleTier = rule.tiers[2];
                expect(ruleTier).toBeDefined();
                expect(ruleTier.id).toBe(5);
                expect(ruleTier.ordinal).toBe(3);

                // Retrieve and check the next rule tier by ordinal
                let previousRuleTier = findPreviousRuleTier(rule, ruleTier);
                expect(previousRuleTier).toBeDefined();
                expect(previousRuleTier.id).toBe(4);
                expect(previousRuleTier.ordinal).toBe(2);
            });

            test("should return null given null input", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                let previousRuleTier = findPreviousRuleTier(rule, null);
                expect(previousRuleTier).toBeNull();
            });

            test("should return null given undefined input", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                let previousRuleTier = findPreviousRuleTier(rule, undefined);
                expect(previousRuleTier).toBeNull();
            });

            test("should return null given an invalid object", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                let previousRuleTier = findPreviousRuleTier(rule, {});
                expect(previousRuleTier).toBeNull();
            });
        });

        describe("Find next", () => {
            test("should return the correct rule tier given a valid rule tier", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                // Retrieve and check the rule tier
                let ruleTier = rule.tiers[2];
                expect(ruleTier).toBeDefined();
                expect(ruleTier.id).toBe(5);
                expect(ruleTier.ordinal).toBe(3);

                // Retrieve and check the next rule tier by ordinal
                let nextRuleTier = findNextRuleTier(rule, ruleTier);
                expect(nextRuleTier).toBeDefined();
                expect(nextRuleTier.id).toBe(6);
                expect(nextRuleTier.ordinal).toBe(4);
            });

            test("should return null given null input", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                let nextRuleTier = findNextRuleTier(rule, null);
                expect(nextRuleTier).toBeNull();
            });

            test("should return null given undefined input", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                let nextRuleTier = findNextRuleTier(rule, undefined);
                expect(nextRuleTier).toBeNull();
            });

            test("should return null given an invalid object", () => {
                // Get the rule
                let rule = findRuleById(44);
                expect(rule).toBeDefined();
                expect(rule.id).toBe(44);
                expect(rule.ordinal).toBe(2);
                expect(rule.tiers).toBeDefined();

                let nextRuleTier = findNextRuleTier(rule, {});
                expect(nextRuleTier).toBeNull();
            });
        });

        describe("Resequence ordinals", () => {
            test("should ensure that ordinals are sequential, starting with 1, after middle rule is deleted", () => {
                let rulesetI = 3;
                let ruleI = 1;
                let tierI = 2;

                setParentState(dialogStates.modes.edit, dialogStates.entityTypes.tieredRateRule, app.jurisdictionRules[rulesetI].rules[ruleI]);
                // Get the rule tier we are going to delete
                let deletedTier = app.jurisdictionRules[rulesetI].rules[ruleI].tiers[tierI];

                expect(deletedTier.id).toBe(5);
                expect(deletedTier.ordinal).toBe(3);

                // Now delete the rule tier from the list
                expect(app.jurisdictionRules[rulesetI].rules[ruleI].tiers.length).toBe(4);
                app.jurisdictionRules[rulesetI].rules[ruleI].tiers.splice(tierI, 1);
                expect(app.jurisdictionRules[rulesetI].rules[ruleI].tiers.length).toBe(3);

                // Now resequence the ordinals
                let tiers = resequenceRuleTierOrdinals(deletedTier);
                expect(tiers[0].id).toBe(3);
                expect(tiers[0].ordinal).toBe(1);

                expect(tiers[1].id).toBe(4);
                expect(tiers[1].ordinal).toBe(2);

                expect(tiers[2].id).toBe(6);
                expect(tiers[2].ordinal).toBe(3);
            });
        });
    });
});