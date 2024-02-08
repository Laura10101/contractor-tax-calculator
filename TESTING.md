# Testing

## Browser Compatability

## Code Validation

### HTML Validation

### CSS Validation

### JavaScript Validation

## Responsiveness

## User Story Tests

## API Tests

The main functionality for the tax calculator has been implemented across five different APIs. Collectively, these APIs comprise X complex model methods and more than 35 services. Each service is also exposed through a single API endpoint. While the API endpoints and services mostly provide basic CRUD functionality for different models, the rule calculations endpoint and service comprises more complex algorithms.

Given the scope of this project, comprehensively verifying the correctness of these services and methods through manual testing would not be feasible within a realistic timescale. I therefore opted to implement good automated test coverage across the APIs. 

To achieve this, testing was implemented at three levels:

1. **Model Tests** focus on testing the correctness of complex model methods. These tests assume that the model data has been validated by services and views and so aim to test whether the methods produce the correct output given valid input data.
2. **Services Tests** focus on testing the correctness of the services exposed by any API. These tests ensure that services are properly validating the input data they receive, that the database is correctly updated or read depending, and that any necessary model or third-party functionality is correctly called.
3. **Views Tests** focus on testing the correctness of the APIView methods to ensure that the incoming request is appropriately validated, that the appropriate service is invoked and completes as expected, that any response data is appropriately serialised and that the expected response and status code is therefore returned by the API.

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

### Resolved Bugs
A total of 222 bugs were identified and resolved during testsing for this project.

For a complete list of these resolved bugs, please see [BUGS.MD](BUGS.MD).

Alternatively, you can view the original list of resolved Github Bugs [here](https://github.com/Laura10101/contractor-tax-calculator/issues?q=is%3Aissue+is%3Aclosed).

### Unresolved Bugs
