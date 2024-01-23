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

describe("View model accessor methods", () => {
    beforeEach(() => {
        appState = buildAppState();
        app.jurisdictions = appState.jurisdictions;
        app.taxCategories = appState.taxCategories;
        app.jurisdictionForm = appState.jurisdictionForm;
        app.jurisdictionRules = appState.jurisdictionRules;
    });

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
});

describe("Ordinal traversal and management", () => {

});