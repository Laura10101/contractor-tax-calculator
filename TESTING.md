# Testing

## Browser Compatability

## Code Validation

### HTML Validation

### CSS Validation

### JavaScript Validation

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
![Pytest results for API tests](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/api-test-results.jpg)

These 600 tests provide 83% coverage across the five APIs as shown below. The following coverage report was generated using the Python coverage library:

![Test coverage report for API tests](https://laura10101.github.io/contractor-tax-calculator/documentation/screenshots/api-test-coverage.jpg)

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
