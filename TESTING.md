# Testing

## User Story Testing

### As an IT contractor  I want to…..
1. [Select the jurisdictions to compare tax calculations for, so that I only see jurisdictions I am interested in](https://github.com/Laura10101/contractor-tax-calculator/issues/1)
  - The user selections jurisdictions using the `Select Jurisdictions` form as shown below.
  - The `Next` button is disabled until at least one jurisdiction has been selected.
  ![The select jurisdiction form](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/select-jurisdictions.png)
  - Once a selection has been made, the form can be submitted.
  ![The select jurisdiction form](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/select-jurisdictions-selected.png)

2. [Easily enter my income details, so that my tax can be calculated for each jurisdiction I have selected](https://github.com/Laura10101/contractor-tax-calculator/issues/2)
  - The user enters their financial information using the `Financial Information` form as shown below.
  - The form guides the user through the process of responding to these questions.
  - The form displays validation errors clearly to the user and the form will not be submitted if validation errors are displayed.
  ![The financial info form](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/financial-info-errors.png)
  - Once all errors are cleared, the form can be submitted.
  ![The financial info form](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/financial-info.png)

3. [See how much progress I am making while using the application, so that I can easily see where I am in the process](https://github.com/Laura10101/contractor-tax-calculator/issues/3)
   - The user can see their progress through the application using the breadcrumb provided at the top of Tax Calculation journey pages.
   ![The breadcrumb](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/breadcrumb.png)

4. [See a clear tax calculation for each jurisdiction I have selected that is easy to understand, so that I can easily decide which jurisdiction is most favourable](https://github.com/Laura10101/contractor-tax-calculator/issues/4)
   - The user views their tax calculation results on the `Calculation Results` page as shown below.
   - For each jurisdiction that was included in the calculation, a card is displayed providing a summary of the tax to be paid.
  ![The calculation results page](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/calculation-results.png)
  - The user can click the *View Details* button in order to see the detailed steps taken to calculate tax due for that Jurisdiction.
  ![The calculation results page](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/calculation-result-details.png)


5. [Have my data be protected by login and appropriate security measures, so that I have confidence only I can access the data](https://github.com/Laura10101/contractor-tax-calculator/issues/5)
   - Any attempt to access a Contractor restricted page without logging in first redirects the user to the Login form.
   - Here the user attempts to access the contractor dashboard while not logged in.
   ![Forcing contractor login](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/force-contractor-login-1.png)
   - They are redirected as shown to the login form.
   ![Forcing contractor login](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/force-contractor-login-2.png)


6. [Purchase subscriptions for the tax calculator, so that I can begin comparing my tax calculations right away](https://github.com/Laura10101/contractor-tax-calculator/issues/6)
   - When the user is signed into account with no active subscription, they can purchase a subscription by first clicking the link on the Contractor dashboard.
   ![Purchasing a subscription](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/contractor-dashboard-new-user.png)
   - Then the user selects their subscription option.
   ![The subscription options form](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/subscription-options.png)
   - Finally, they complete the checkout form.
   ![The checkout form](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/checkout.png)
   - Once payment has completed...
   ![The payment status page](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/payment-status.png)
   - Return to the contractor dashboard to confirm that your subscription is now active.
   ![Purchasing a subscription](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/contractor-dashboard.png)

### As the Contractor Tax Calculator team, I want...
7. [Non-admin users to be prevented from creating tax calculations without an active subscription, so that I can generate an income](https://github.com/Laura10101/contractor-tax-calculator/issues/7)
   - Attempting to create a tax calculation without a subscription will redirect the user to the subscription option page.
   ![Forcing contractor subscription](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/force-subscription-1.png)
   ![Forcing contractor subscription](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/force-subscription-2.png)

### As an admin user I want to….
8. [Add new jurisdictions, so that I can continuously improve the product](https://github.com/Laura10101/contractor-tax-calculator/issues/8)
   - The user can add a new Jurisdiction by first visiting the `Jurisdictions` page in the basic admin app.
   ![Creating a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions.png)
   - The user can then choose to create a new Jurisdiction and complete the form.
   ![Creating a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions-create.png)
   - The `Jurisdictions` page will now display the new Jurisdiction.
   ![Creating a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions-create-success.png)

9. [Delete jurisdictions, so that I can continuously improve the product](https://github.com/Laura10101/contractor-tax-calculator/issues/9)
   - The user can delete a Jurisdiction by first visiting the `Jurisdictions` page in the basic admin app.
   ![Deleting a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions.png)
   - The user can then choose to delete a Jurisdiction and confirm the action.
   ![Deleting a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions-delete.png)
   - The `Jurisdictions` page will no longer display the new Jurisdiction.
   ![Deleting a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions-delete-success.png)

10. [Define the questions that IT contractors should be asked for a given jurisdiction - and the format of the corresponding answer fields - so that the tax calculator will display only relevant questions to users](https://github.com/Laura10101/contractor-tax-calculator/issues/10)
  - To create a new question for the selected jurisdiction, the users first choose the type of question they wish to create.
  ![Creating questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-question-type.png)
  - The user then fills out the Create Question form as instructed on screen and clicks "Save Changes".
  ![Creating questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-create-question-errors.png)
  - A success message is displayed.
  ![Creating questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-create-question-success.png)
  - The question is then displayed.
  ![Creating questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-create-question-display.png)
  - To add a multiple choice option, the user must first select to edit a multiple choice question from the Questions display, as described above.
  - Multiple choice options can only be added when the question is being edited (not created).
  - Click the *Add Option* button at the bottom of the `Multiple Choice Question` form.
  ![Editing questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-edit-question.png)
  - Complete the form that is displayed and click *Save Changes*.
  ![Creating multiple choice options in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-add-option.png)
  - A success message is displayed:
  ![Creating multiple choice options in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-add-option-success.png)
  - The new option is displayed in the table on the `Edit Question` page.
  ![Creating multiple choice options in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-add-option-displayed.png)

11. [Edit the questions and answer formats associated with a given jurisdiction at any time, so that I can keep the tax calculator up to date with changes in tax regimes](https://github.com/Laura10101/contractor-tax-calculator/issues/11)
   - To edit an existing question, the user selects the Edit button next to a question and then completes the form that is displayed.
  ![Editing questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-edit-question.png)
  - A success message is then displayed.
  ![Editing questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-edit-question-success.png)
  - The updated question is displayed.
  ![Editing questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-edit-question-displayed.png)

12. [Questions and answer formats that are associated with a jurisdiction to be deleted if the jurisdiction itself is deleted, so that I do not store redundant data in the database](https://github.com/Laura10101/contractor-tax-calculator/issues/12)
   - I delete a Jurisdiction as per the instructions above.
   - Check in the database to confirm that no form is associated with that Jurisdiction.
   ![Deleting a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions-delete-forms.png)

13. [Create the tax rates for a jurisdiction, so that I can add new jurisdictions to improve the product](https://github.com/Laura10101/contractor-tax-calculator/issues/13)
   - To create a new ruleset, the user clicks the *+ Ruleset* button at the top of the config app.
   - The user then selects a tax category to create the ruleset for.
   ![Creating a ruleset in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-ruleset-tax-category.png)
   - A success message is then displayed.
   ![Creating a ruleset in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-ruleset-success.png)
   - And the ruleset is displayed within the rulesets display.
   ![Creating a ruleset in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-ruleset-displayed.png)
   - To add a rule, the user clicks the *+* button in the title bar for the Ruleset to which the rule should be added.
   - The user then chooses a Rule Type.
   ![Creating a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-type.png)
   - The user then fills out the `Create Rule` form that is displayed and then clicks *Save Changes*.
   ![Creating a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-create.png)
   - A success message is then displayed.
   ![Creating a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-create-success.png)
   - And the rule is displayed in the rulesets display.
   ![Creating a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-create-displayed.png)


14. [Update tax rates for a jurisdiction, so that I can keep the product up to date with changing tax regimes](https://github.com/Laura10101/contractor-tax-calculator/issues/14)
   - To edit a rule, the user clicks the Edit Rule button next to any rule in the Rulesets display.
   - From here, they complete the form that is displayed and click *Save Changes*
   ![Editing a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-edit.png)
   - A success message is then displayed.
   ![Editing a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-edit-success.png)
   - And the rule is updated in the rulesets display.
   ![Editing a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-edit-displayed.png)

15. [Tax rates for a jurisdiction to be deleted if the jurisdiction is deleted, so that I do not store unnecessary data in the database](https://github.com/Laura10101/contractor-tax-calculator/issues/15)
   - I first delete a jurisdiction as described above.
   - I then check in the database to confirm that there are no rulesets with the deleted jurisdiction's ID.
   ![Deleting a jurisdiction](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-jurisdictions-delete-rulesets.png)

16. [View subscriptions, so that I can assist users with any subscription-related queries](https://github.com/Laura10101/contractor-tax-calculator/issues/16)
   - Admin users can view subscriptions in the `Subscriptions` page of the basic admin app.
   ![Managing subscriptions](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-subscriptions.png)

17. [View payments, so that I can assist users with any payment-related queries](https://github.com/Laura10101/contractor-tax-calculator/issues/17)
   - Admin users can view payments in the `Payments` page of the basic admin app.
   ![Managing payments](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/manage-payments.png)

18. [Admin functionality to be protected by an admin user account, so that only authorised users can modify jurisdiction, form, and tax rate data](https://github.com/Laura10101/contractor-tax-calculator/issues/18)
   - Attempting to access any admin page without logging in first will redirect the user to the login page.
   - Here a logged in user attempts to access the basic admin page by entering the URL.
   ![Forcing admin login](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/force-admin-login-1.png)
   - They are forced to the admin login page.
   ![Forcing admin login](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/force-admin-login-2.png)


19. [View field names for question and rule fields in the config app, so that I can easily understand which data elements relate to which fields](https://github.com/Laura10101/contractor-tax-calculator/issues/237)
   - The field names for questions are displayed for each field in the Questions display of the config app.
   ![Questions in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-questions.png)
   - The field names for rules are displayed for each rule in the Rulesets display of the config app.
   ![Creating a rule in the config app](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/features/config-rule-create-displayed.png)

## Browser Compatability

All user story testing was performed in Edge. All Responsiveness tests were performed in Safari on a iPhone. The following tests confirm that the app works as expected in Chrome and Firefox.

### The Index Page

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/index.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/index.png)

### The Contractor Dashboard

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/contractor-dashboard.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/contractor-dashboard.png)

### The Subscription Options Page

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/subscription-options.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/subscription-options.png)

### The Checkout Form

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/checkout.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/checkout.png)

### The Payment Status Page

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/payment-complete.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/payment-complete.png)

### The Select Jurisdictions Form

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/select-jurisdictions.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/select-jurisdictions.png)

### The Financial Information Form

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/financial-info.png)

- __In Firefox__

![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/financial-info.png)

### The Tax Calculation Results Page

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/calculation-results.png)
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/calculation-results-details.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/calculation-results.png)
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/calculation-results-details.png)

### The Config App - Creating Questions

- __In Chrome__
   - The dialog box:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-question-create.png)
   - The success message
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-question-create-success.png)

- __In Firefox__

   - The dialog box:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-question-create.png)
   - The success message
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-question-create-success.png)

### The Config App - Creating Rulesets

- __In Chrome__
   - Selecting the tax category for the ruleset:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-ruleset-tax-category.png)
   - The success message:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-ruleset-success.png)

- __In Firefox__
   - Selecting the tax category for the ruleset:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-ruleset-tax-category.png)

### The Config App - Creating Rules

- __In Chrome__
   - Entering rule details:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-rule-create.png)
   - The success message:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-rule-create-success.png)

- __In Firefox__
   - Entering rule details:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-rule-create.png)
   - The success message:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-rule-create-success.png)

### The Config App - Editing Rules

- __In Chrome__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-rule-edit.png)

- __In Firefox__
![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-rule-edit.png)

### The Config App - Creating Rule Tiers

- __In Chrome__
   - Entering tier details:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-tier-create.png)
   - The success message:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/chrome/config-tier-create-success.png)

- __In Firefox__
   - Entering tier details:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-tier-create.png)
   - The success message:
   ![Browser compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/browser-testing/firefox/config-tier-create-success.png)

## Code Validation

### HTML Validation
All custom HTML passes validation as shown below. The only warning that I ignored related to some section elements not having a heading.

__The Index Page__
![HTML validation for index page](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/index.png)

__The Contractor Landing Page__
![HTML validation for contractor landing page](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/contractor-landing.png)

__The Contractor Dashboard__
![HTML validation for contractor dashboard](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/contractor-dashboard.png)

__The Subscription Options Page__
![HTML validation for subscription options form](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/subscription-options.png)

__The Checkout Form__
![HTML validation for checkout form](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/checkout.png)

__The Payment Status Page__
![HTML validation for select jurisdictions form](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/payment-status.png)

__The Select Jurisdictions Form__
![HTML validation for select jurisdictions form](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/select-jurisdictions.png)

__The Financial Information Form__
![HTML validation for financial info form](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/financial-info.png)

__The Tax Calculation Results Page__
![HTML validation for calculation results page](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/calculation-results.png)

__The Admin Landing Page__
![HTML validation for admin landing page](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/admin-landing.png)

__The Config App__
![HTML validation for config app](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/html/config.png)

### CSS Validation
All custom CSS is contained within my base.css file as part of the base template. This file validates successfully as shown below:

![CSS validation for base.css](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/css/css-validation.png)

### JavaScript Validation
For this project, I developed custom JavaScript to provide enhanced user experiences in four areas:

- To validate user input on the financial information form when creating a tax calculation.
- To provide Stripe integration through the card and address elements on the checkout page.
- To provide a single-page configuration experience for managing tax questions and rates in the config app. This JavaScript is separated into five files as follows:
   - **views.js** provides the event handlers and action methods that provide the functionality for each component of the user interface.
   - **view_utils.js** provides a set of utility functions for DOM manipulation and data validation. These cover controlling Bootstrap modals, validating user input, and displaying models returned by the API to the user.
   - **view_models.js** provide a set of functions used for managing application state. This includes storing and refreshing referential data (Jurisdictions and Tax Categories), query methods to retrieve objects from the app state by ID or other attributes, and commands for managing entity ordinals.
   - **view_consts.js** define constants used by the other layers of JavaScript. These constants include API endpoints for different actions and IDs of important DOM elements.
   - **service_clients.js** define a set of functions that provide easier access to the APIs via a set of JQuery AJAX requests.
- To test the various layers of the config app's JavaScript. There is a test file for each layer (except view_consts.js, which contains no functionality). There is also a file containing mock data.

Additionally, custom JavaScript is used to implement the Jest testing for the config app.

All custom JavaScript passes validation without errors as shown below.

There are a number of undefined and unused variables in each of the files. These relate to variables which are either imported to, or exported from, JavaScript modules.

**Validating user input - validation.js**

![JSHint validation for validation.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/validation-js-validation.png)

**Stripe integration - stripe_elements.js**

![JSHint validation for stripe_elements.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/stripe-elements-js-validation.png)

**Config app - views.js**

![JSHint validation for views.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/views-validation.png)

One warning is highlighted here. This calls out the fact that the confirm() function is overridden by a custom confirm() function. I decided to ignore this warning since the custom confirm() function fulfills the same purpose as JavaScript's built-in confirm() function which is to display a dialog asking a user to confirm an action.

**Config app - views.test.js**

![JSHint validation for views.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/views-test-js-validation.png)

**Config app - view_utils.js**

![JSHint validation for view_utils.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-utils-js-validation.png)

**Config app - view_utils.test.js**

![JSHint validation for view_utils.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/views-utils-test-js-validation.png)

Two warnings are highlighted here. The first calls out the fact that the confirm() function is overridden by a custom confirm() function. I decided to ignore this warning since the custom confirm() function fulfills the same purpose as JavaScript's built-in confirm() function which is to display a dialog asking a user to confirm an action.

The second warning relates to the use of document.write() to populate the DOM when setting up a mock DOM for Jest testing. The code to do this was taken from the Code Institute's videos on testing with Jest, and so I decided not to look for an alternative solution.

**Config app - view_models.js**

![JSHint validation for view_models.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-models-js-validation.png)

**Config app - view_models.test.js**

![JSHint validation for view_models.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/views-models-test-js-validation.png)

**Config app - view_models.mocks.js**

![JSHint validation for view_models.mocks.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-models-mocks-js-validation.png)

**Config app - view_consts.js**

![JSHint validation for view_consts.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-utils-js-validation.png)

**Config app - service_clients.js**

![JSHint validation for service_clients.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/service-clients-js-validation.png)

**Config app - service_clients.test.js**

![JSHint validation for service_clients.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/service-clients-test-js-validation.png)

### Python validation (PEP8)

**Settings**
- The main `settings.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/settings/settings_py.png)
- The `test_settings.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/settings/test_settings_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/settings/urls_py.png)

**Utilities**
- The main `custom_storages.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/utilities/custom_storages_py.png)
- The `jest_test_setup.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/utilities/jest_test_setup_py.png)
- The `django_test_setup.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/utilities/django_test_setup_py.png)
- The `json_to_markdown.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/utilities/json_markdown_py.png)

**Calculations App**
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/calculations/apps_py.png)
- The `helpers.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/calculations/helpers_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/calculations/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/calculations/views_py.png)

**Checkout App**
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/checkout/apps_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/checkout/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/checkout/views_py.png)

**Config App**
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/config/apps_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/config/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/config/views_py.png)

**Home App**
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/home/apps_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/home/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/home/views_py.png)

**Subscription App**
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/subscriptions/apps_py.png)
- The `helpers.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/subscriptions/helpers_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/subscriptions/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apps/subscriptions/views_py.png)

**Forms API**
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/apps_py.png)
- The `models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/models_py.png)
- The `serializers.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/serializers_py.png)
- The `signals.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/signals_py.png)
- The `services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/services_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/views_py.png)
- The `test_services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/test_services_py.png)
- The `test_views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/forms/test_views_py.png)

**Jurisdictions API**
- The `admin.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/admin_py.png)
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/apps_py.png)
- The `autocompletes.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/autocompletes_py.png)
- The `models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/models_py.png)
- The `serializers.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/serializers_py.png)
- The `services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/services_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/views_py.png)
- The `test_services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/test_services_py.png)
- The `test_views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/jurisdictions/test_views_py.png)

**Payments API**
- The `admin.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/admin_py.png)
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/apps_py.png)
- The `formss.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/forms_py.png)
- The `models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/models_py.png)
- The `services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/services_py.png)
- The `stripe.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/stripe_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/views_py.png)
- The `test_services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/test_services_py.png)
- The `test_views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/payments/test_views_py.png)

**Rules API**
- The `admin.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/admin_py.png)
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/apps_py.png)
- The `models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/models_py.png)
- The `services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/services_py.png)
- The `signals.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/signals_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/views_py.png)
- The `test_models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/test_models_py.png)
- The `test_calculations.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/test_calculations_py.png)
- The `test_services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/test_services_py.png)
- The `test_views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/rules/test_views_py.png)

**Subscriptions API**
- The `admin.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/admin_py.png)
- The `apps.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/apps_py.png)
- The `autocompletes.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/autocompletes_py.png)
- The `forms.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/forms_py.png)
- The `models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/models_py.png)
- The `signals.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/signals_py.png)
- The `services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/services_py.png)
- The `urls.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/urls_py.png)
- The `views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/views_py.png)
- The `test_models.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/test_models_py.png)
- The `test_services.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/test_services_py.png)
- The `test_views.py` file:
![PEP8 validation](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/python/apis/subscriptions/test_views_py.png)

## Responsiveness

### The Index Page
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/index.png)

### The Contractor Dashboard
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/contractor-dashboard.png)

### The Subscription Options Page
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/subscription-options.png)

### The Checkout Form
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/checkout.png)

### The Payment Status Page
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/payment-status.png)

### The Select Jurisdictions Form
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/select-jurisdictions.png)

### The Financial Information Form
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/financial-info.png)

### The Tax Calculation Results Page
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/calculation-results.png)
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/calculation-results-details.png)

### The Config App - Questions Display
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-questions.png)

### The Config App - Creating Questions
- Selecting a question type:
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-question-type.png)
- Entering question details:
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-question-create.png)

### The Config App - Rulesets Display
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-rulesets.png)

### The Config App - Creating Rulesets
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-ruleset-tax-category.png)

### The Config App - Creating Rules
- Selecting a rule type:
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-rule-type.png)
- Entering the rule details:
![Mobile compatibility testing](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/responsiveness/config-create-rule.png)

## JavaScript Tests

### Running the Jest tests
To fully test the Config app, I have developed four Jest tests suites to cover each of the functional layeres of the config app's JavaScript. One of these - the **service_clients.test.js** test suite - checks that the service clients correctly interact with the APIs. In order for this to work correctly without adding test data into the production system, a couple of steps must be taken to set up the APIs in test mode.

1. Follow the `Local Deployment` steps as described in the [README](README.md).
2. In `env.py`, make sure that the `os.environ['USE_TEST_DB']` setting is set to `True`.
3. Run the following three commands shown below in the Gitpod terminal. The first command runs the `jest_test_setup` script which tears down the existing test database and recreates it with some basic test data.
```console
python jest_test_setup.py
python manage.py runserver
npm test
```
4. To repeat the tests, run the following two commands (no need to run the Django server again).
```console
python jest_test_setup.py
npm test
```
5. Once done with testing, change the `os.environ['USE_TEST_DB']` setting back to `False` in `eny.py`.
6. Finally, re-run the Django server to return to using the production database.
```console
python manage.py runserver
```

### Overview of Results
The JavaScript underpinning the config app was highly complex and so testing all of the scenarios supported by the config app was not possible manually. I therefore developed a suite of JavaScript automated tests using Jest.

The JavaScript for the config app is organised into four layers as described below:

- **views.js** provides the event handlers and action methods that provide the functionality for each component of the user interface.
- **view_utils.js** provides a set of utility functions for DOM manipulation and data validation. These cover controlling Bootstrap modals, validating user input, and displaying models returned by the API to the user.
- **view_models.js** provide a set of functions used for managing application state. This includes storing and refreshing referential data (Jurisdictions and Tax Categories), query methods to retrieve objects from the app state by ID or other attributes, and commands for managing entity ordinals.
- **view_consts.js** define constants used by the other layers of JavaScript. These constants include API endpoints for different actions and IDs of important DOM elements.
- **service_clients.js** define a set of functions that provide easier access to the APIs via a set of JQuery AJAX requests.

I therefore organiseed my Jest tests for the config app into four suites with each suite testing one of the layers above, with the exception of the view_consts layer since this contains no functionality.

The four test suites comprise 259 tests, achieving overall coverage across the five layers of 83% of functions and 92% of statements.

All of these tests are currently passing as shown below.

![JSHint validation for views.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/views-validation.png)

## API Tests

The main functionality for the tax calculator has been implemented across five different APIs, each managing the data and services associated with a different data domain. Each API was separated into a number of logical layers as described in the [README](README.md):

- **Views** which handle validation and serialisation of HTTP requests and responses.
- **Services** which orchestrate the functionality needed for specific actions.
- **Models** which define the data models that the API manages and provides atomic methods to manipulate those data models.

Given the scope of this project, comprehensively verifying the correctness of these services and methods through manual testing would not be feasible within a realistic timescale. I therefore opted to implement good automated test coverage across the APIs. 

To achieve this, I decided to test each layer of this architecture individually as follows:

- **Views Tests** which focus on the validation and serialisation logic provided by each view in the API.
- **Service Tests** which focus on ensuring that each service correctly delivers the expected behaviour of the particular API method (for example, payments are confirmed with Stripe providing the card details are valid).
- **Model Tests** which focus on testing individual model methods where these are sufficiently complex to justify this level of testing (for exmaple, in the case of the calculations functionality).

In total, I developed 600 tests covering each of the five APIs which are all passing as shown below:
![Pytest results for API tests](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/api-testing/api-test-results.jpg)

These 600 tests provide 83% coverage across the five APIs as shown below. The following coverage report was generated using the Python coverage library:

![Test coverage report for API tests](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/api-testing/api-test-coverage.jpg)

## Bugs
All bugs found during testing for this project were tracked using the Issues feature in Github.

### Resolved Bugs
A total of 222 bugs were identified and resolved during testsing for this project.

For a complete list of these resolved bugs, please see [BUGS.MD](BUGS.MD).

Alternatively, you can view the original list of resolved Github Bugs
<a href="https://github.com/Laura10101/contractor-tax-calculator/issues?q=is%3Aissue+is%3Aclosed+label%3Abug" target="_blank">here</a>.

### Unresolved Bugs
213. **[Deleting entities results in a database error: too many connections](https://github.com/Laura10101/contractor-tax-calculator/issues/213)**<br/>When a significant number of questions, rules or tiers have been added against a single jurisdiction, ruleset, or rule respectively, then deleting an entity causes the following error:<br/>FATAL: too many connections for role "mqrlkcwy"<br/>**Root Cause**<br/>Deleting any of the objects above causes rulesets to be resequenced. This involves updating the ordinal on each question which was not deleted to ensure they remain sequential. Each request is sent asynchronously, allowing for multiple requests to be sent in parallel. Consequently, where there is a large number of entities to be resequenced, the number of requests sent in parallel may exceed the number of allowed connections.<br/>**Justification for not resolving this bug**<br/>I have attempted to resolve this in a couple of different ways. Firstly, I attempted to configure Django to immediately close database connections once they were no longer in use. I have also added to the service clients in the config app a mechanism to batch update requests when swapping ordinals so that each batch is only processed once the previous batch completed. I have also engaged with the Code Institute tutors but have not yet been able to solve the problem.