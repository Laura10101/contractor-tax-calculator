/*
 * view_models.js
 * Holds the current state of the config app, providing global access
 * to state data 
 */
let app = {
    jurisdictions: [],
    taxCategories: [],
    jurisdictionForm: {},
    jurisdictionRules: [],
    dialogState: {
        mode: null,
        entityType: null,
        entity: null
    }
}

function clearDialogState() {
    app.dialogState = {

    };
}

function setDialogState(mode, entityType, entity) {
    app.dialogState = {
        mode: mode,
        entityType: entityType,
        entity: entity
    };
}

function getTaxCategoryById(id) {
    let category = null;
    app.taxCategories.forEach(taxCategory => {
        if (taxCategory.tax_category_id == id) {
            category = taxCategory;
        }
    });
    return category;
}