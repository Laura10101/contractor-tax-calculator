# Testing

## User Story Testing

### As an IT contractor  I want to…..
1. [Select the jurisdictions to compare tax calculations for, so that I only see jurisdictions I am interested in](https://github.com/Laura10101/contractor-tax-calculator/issues/1)
   - The user selections jurisdictions using the `Select Jurisdictions` form as shown below.

2. [Easily enter my income details, so that my tax can be calculated for each jurisdiction I have selected](https://github.com/Laura10101/contractor-tax-calculator/issues/2)
   - The user enters their financial information using the `Financial Information` form as shown below.

3. [See how much progress I am making while using the application, so that I can easily see where I am in the process](https://github.com/Laura10101/contractor-tax-calculator/issues/3)
   - The user can see their progress through the application using the breadcrumb provided at the top of Tax Calculation journey pages.

4. [See a clear tax calculation for each jurisdiction I have selected that is easy to understand, so that I can easily decide which jurisdiction is most favourable](https://github.com/Laura10101/contractor-tax-calculator/issues/4)
   - The user views their tax calculation results on the `Calculation Results` page as shown below.

5. [Have my data be protected by login and appropriate security measures, so that I have confidence only I can access the data](https://github.com/Laura10101/contractor-tax-calculator/issues/5)
   - Any attempt to access a Contractor restricted page without logging in first redirects the user to the Login form.

6. [Purchase subscriptions for the tax calculator, so that I can begin comparing my tax calculations right away](https://github.com/Laura10101/contractor-tax-calculator/issues/6)
   - When the user is signed into account with no active subscription, they can purchase a subscription by first clicking the link on the Contractor dashboard.
   - Then the user selects their subscription option.
   - Finally, they complete the checkout form.
   - Once payment has completed...
   - Return to the contractor dashboard to confirm that your subscription is now active.

### As the Contractor Tax Calculator team, I want...
7. [Non-admin users to be prevented from creating tax calculations without an active subscription, so that I can generate an income](https://github.com/Laura10101/contractor-tax-calculator/issues/7)
   - Attempting to create a tax calculation without a subscription will redirect the user to the subscription option page.

### As an admin user I want to….
8. [Add new jurisdictions, so that I can continuously improve the product](https://github.com/Laura10101/contractor-tax-calculator/issues/8)
   - The user can add a new Jurisdiction by first visiting the `Jurisdictions` page in the basic admin app.
   - The user can then choose to create a new Jurisdiction and complete the form.
   - The `Jurisdictions` page will now display the new Jurisdiction.

9. [Delete jurisdictions, so that I can continuously improve the product](https://github.com/Laura10101/contractor-tax-calculator/issues/9)
   - The user can delete a Jurisdiction by first visiting the `Jurisdictions` page in the basic admin app.
   - The user can then choose to delete a Jurisdiction and confirm the action.
   - The `Jurisdictions` page will no longer display the new Jurisdiction.

10. [Define the questions that IT contractors should be asked for a given jurisdiction - and the format of the corresponding answer fields - so that the tax calculator will display only relevant questions to users](https://github.com/Laura10101/contractor-tax-calculator/issues/10)
   - The user can add a new question by choosing the *+ Question* button at the top of the Config app.
   - The user then chooses a Question type.
   - The user then completes the `Create Question` form as displayed and clicks *Save Changes*
   - The new question will now be displayed.

11. [Edit the questions and answer formats associated with a given jurisdiction at any time, so that I can keep the tax calculator up to date with changes in tax regimes](https://github.com/Laura10101/contractor-tax-calculator/issues/11)
   - To edit a Question and its answer format, the user clicks the *Edit Question* icon next to any question.
   - The user completes the `Edit Question` form as displayed and clicks *Save Changes*
   - The updated question will be displayed.

12. [Questions and answer formats that are associated with a jurisdiction to be deleted if the jurisdiction itself is deleted, so that I do not store redundant data in the database](https://github.com/Laura10101/contractor-tax-calculator/issues/12)
   - I delete a Jurisdiction as per the instructions above.
   - Check in the database to confirm that no form is associated with that Jurisdiction.

13. [Create the tax rates for a jurisdiction, so that I can add new jurisdictions to improve the product](https://github.com/Laura10101/contractor-tax-calculator/issues/13)
   - To create the tax rates for a Jurisdiction, the user first chooses to create a new ruleset by clicking the *+ Ruleset* button in the config app.
   - The user selects the tax category for the new ruleset and then clicks *Save Changes*
   - The user can now add rules to the ruleset by clicking the *+* button at the top of the ruleset to which the rule should be added.
   - The user selects the type of rule to be created.
   - They then complete the form as displayed and click *Save Changes*.
   - The new rule will be displayed in the rulesets display.
   - Tiers can be added to `Tiered Rate` or `Tiered Rate with Progression` rules by editing an existing rule.
   - The user then clicks the *+ Tier* button at the bottom of the `Edit Question` form.
   - The user then fills out the `Create Tier` form and clicks *Save Changes*.
   - The new tier will be displayed.

14. [Update tax rates for a jurisdiction, so that I can keep the product up to date with changing tax regimes](https://github.com/Laura10101/contractor-tax-calculator/issues/14)
   - The user can update tax rates by clicking the *Edit* button next to any rule.
   - The user then completes the `Edit Rule` form as displayed and clicks *Save Changes*.
   - The updated rule details are displayed in the rule display.

15. [Tax rates for a jurisdiction to be deleted if the jurisdiction is deleted, so that I do not store unnecessary data in the database](https://github.com/Laura10101/contractor-tax-calculator/issues/15)
   - I first delete a jurisdiction as described above.
   - I then check in the database to confirm that there are no rulesets with the deleted jurisdiction's ID.

16. [View subscriptions, so that I can assist users with any subscription-related queries](https://github.com/Laura10101/contractor-tax-calculator/issues/16)
   - Admin users can view subscriptions in the `Subscriptions` page of the basic admin app.

17. [View payments, so that I can assist users with any payment-related queries](https://github.com/Laura10101/contractor-tax-calculator/issues/17)
   - Admin users can view payments in the `Payments` page of the basic admin app.

18. [Admin functionality to be protected by an admin user account, so that only authorised users can modify jurisdiction, form, and tax rate data](https://github.com/Laura10101/contractor-tax-calculator/issues/18)
   - Attempting to access any admin page without logging in first will redirect the user to the login page.

19. [View field names for question and rule fields in the config app, so that I can easily understand which data elements relate to which fields](https://github.com/Laura10101/contractor-tax-calculator/issues/237)
   - The field names for questions are displayed for each field in the Questions display of the config app.
   - The field names for rules are displayed for each rule in the Rulesets display of the config app.

## Browser Compatability

All user story testing was performed in Edge. All Responsiveness tests were performed in Safari on a iPhone. The following tests confirm that the app works as expected in Chrome and Firefox.

### The Index Page

- __In Chrome__

- __In Firefox__

### The Contractor Landing Page

- __In Chrome__

- __In Firefox__

### The Admin Landing Page

- __In Chrome__

- __In Firefox__

### The Contractor Dashboard

- __In Chrome__

- __In Firefox__

### The Subscription Options Page

- __In Chrome__

- __In Firefox__

### The Checkout Form

- __In Chrome__

- __In Firefox__

### The Select Jurisdictions Form

- __In Chrome__

- __In Firefox__

### The Financial Information Form

- __In Chrome__

- __In Firefox__

### The Tax Calculation Results Page

- __In Chrome__

- __In Firefox__

### The Config App - Creating Questions

- __In Chrome__

- __In Firefox__

### The Config App - Creating Multiple Choice Options

- __In Chrome__

- __In Firefox__

### The Config App - Creating Rulesets

- __In Chrome__

- __In Firefox__

### The Config App - Creating Rules

- __In Chrome__

- __In Firefox__

### The Config App - Creating Rule Tiers

- __In Chrome__

- __In Firefox__

### The Config App - Creating Secondary Rule Tiers

- __In Chrome__

- __In Firefox__

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

**Calculations App**

**Checkout App**

**Config App**

**Home App**

**Subscription App**

**Forms API**

**Jurisdictions API**

**Payments API**

**Rules API**

**Subscriptions API**

## Responsiveness

### The Index Page

### The Contractor Landing Page

### The Admin Landing Page

### The Contractor Dashboard

### The Subscription Options Page

### The Checkout Form

### The Select Jurisdictions Form

### The Financial Information Form

### The Tax Calculation Results Page

### The Config App - Creating Questions

### The Config App - Creating Multiple Choice Options

### The Config App - Creating Rulesets

### The Config App - Creating Rules

### The Config App - Creating Rule Tiers

### The Config App - Creating Secondary Rule Tiers

## JavaScript Tests

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

### Forms API Tests ###

**Services Tests**
The following table lists the services tests for the Forms API. These tests can be found in forms_api/test_services.py while the asscoiated services can be found in forms_api/services.py.

| Test Name | Tested Service | Test Scenario | Expected Result |
| --------- | -------------- | ------------- | --------------- |
| 

**Views Tests**

### Jurisdiction API Tests ###

### Payments API Tests ###

### Rules API Tests ###

### Subscription API Tests ###

## Bugs
All bugs found during testing for this project were tracked using the Issues feature in Github.

### Resolved Bugs
A total of 222 bugs were identified and resolved during testsing for this project.

For a complete list of these resolved bugs, please see [BUGS.MD](BUGS.MD).

Alternatively, you can view the original list of resolved Github Bugs
<a href="https://github.com/Laura10101/contractor-tax-calculator/issues?q=is%3Aissue+is%3Aclosed+label%3Abug" target="_blank">here</a>.

### Unresolved Bugs
