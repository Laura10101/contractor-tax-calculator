# Testing

## Browser Compatability

## Code Validation

### HTML Validation

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

**Config app - views.test.js**

![JSHint validation for views.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/views-test-validation.png)

**Config app - view_utils.js**

![JSHint validation for view_utils.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-utils-js-validation.png)

**Config app - view_utils.test.js**

![JSHint validation for view_utils.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-utils-test-js-validation.png)

**Config app - view_models.js**

![JSHint validation for view_models.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-models-js-validation.png)

**Config app - view_models.test.js**

![JSHint validation for view_models.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-models-test-js-validation.png)

**Config app - view_models.mocks.js**

![JSHint validation for view_models.mocks.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-models-mocks-js-validation.png)

**Config app - view_consts.js**

![JSHint validation for view_consts.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/view-utils-js-validation.png)

**Config app - service_clients.js**

![JSHint validation for service_clients.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/service-clients-js-validation.png)

**Config app - service_clients.test.js**

![JSHint validation for service_clients.test.js](https://laura10101.github.io/contractor-tax-calculator/documentation/validation/js/service-clients-test-js-validation.png)

## Responsiveness

## User Story Tests

## JavaScript Tests

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
