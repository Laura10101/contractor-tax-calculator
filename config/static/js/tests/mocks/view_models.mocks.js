const jurisdictions = [
    { id: 1, name: "All Jurisdictions" },
    { id: 2, name: "France" },
    { id: 3, name: "Germany" },
    { id: 4, name: "Dubai" },
    { id: 5, name: "Japan" }
];

const taxCategories = [
    { tax_category_id: 1, name: "Dividend Tax" },
    { tax_category_id: 2, name: "Corporation Tax" },
    { tax_category_id: 3, name: "Income Tax" },
    { tax_category_id: 4, name: "VAT" }
];

const forms = {
    "forms": {
      "1": {
        id: 1,
        jurisdiction_id: 1,
        questions: [
          {
            id: 3,
            text: "A boolean question test",
            explainer: "Created by automated test",
            is_mandatory: true,
            variable_name: "boolean_var",
            ordinal: 1,
            type: "boolean"
          },
          {
            id: 4,
            text: "A numeric question test",
            explainer: "Created by automated test",
            is_mandatory: true,
            variable_name: "numeric_var",
            ordinal: 1,
            type: "numeric",
            is_integer: true,
            min_value: 1,
            max_value: 100
          },
          {
            id: 7,
            text: "A multiple choice test",
            explainer: "Created by automated test",
            is_mandatory: true,
            variable_name: "multiple_choice_var",
            ordinal: 1,
            type: "multiple_choice",
            options: []
          }
        ]
      }
    }
};

const rules = [

];