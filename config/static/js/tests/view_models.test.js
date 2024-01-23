const { dialogStates } = require("../view_consts");
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

});

describe("View model search functions", () => {

});

describe("Ordinal traversal and management", () => {

});