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

1. **Model Tests** focus on testing the correctness of complex model methods. These tests assume that the model data has been validated by services and views and so aim to test whether the methods produce the correct output given validate input data.
2. **Services Tests** focus on testing the correctness of the services. T

### 

## Bugs

### Resolved Bugs

### Unresolved Bugs
