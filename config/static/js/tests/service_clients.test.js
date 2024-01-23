const { app } = require("../view_models");
const {
    queryToString,
    toUrl,
    getJurisdictions,
    getTaxCategories,
    getFormForJurisdiction,
    createBooleanQuestion,
    updateBooleanQuestion,
    createNumericQuestion,
    updateNumericQuestion,
    createMultipleChoiceQuestion,
    updateMultipleChoiceQuestion,
    updateQuestion,
    removeQuestion,
    postMultipleChoiceOption,
    removeMultipleChoiceOption,
    getRulesetsForJurisdiction,
    postRuleset,
    patchRuleset,
    removeRuleset,
    createFlatRateRule,
    updateFlatRateRule,
    createTieredRateRule,
    updateTieredRateRule,
    createSecondaryTieredRateRule,
    updateSecondaryTieredRateRule,
    removeRule,
    postRuleTier,
    updateRuleTier,
    removeRuleTier,
    postSecondaryRuleTier,
    updateSecondaryRuleTier,
    removeSecondaryRuleTier
} = require("../service_clients");

beforeAll(() => {
    app.apiHost.protocol = "https:";
    app.apiHost.hostname = "8000-laura10101-contractorta-g5o2od5xoex.ws-eu107.gitpod.io";
    jest.useRealTimers();
});

describe("Service client helper functions", () => {
    describe("Query string generation", () => {
        test("should return return valid http query string", () => {
            query = {
                testStringParameter: "abc",
                testIntParameter: 5,
                testBooleanParameter: true
            };
            queryString = queryToString(query);
            expect(queryString).toBe("testStringParameter=abc&testIntParameter=5&testBooleanParameter=true");
        });
    });

    describe("URL generation", () => {
        test("should correctly convert relative endpoint into absolute URL", () => {
            endpoint = "test/";
            url = toUrl(endpoint);
            expect(url).toBe("https://8000-laura10101-contractorta-g5o2od5xoex.ws-eu107.gitpod.io/api/test/");
        });
    });
});

describe("Jurisdiction service client", () => {
    describe("GET", () => {
        test("should correctly retrieve jurisdictions with a 200 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.jurisdictions).toBeDefined();
                data.jurisdictions.forEach(jurisdiction => {
                    expect(jurisdiction.id).toBeDefined();
                    expect(jurisdiction.name).toBeDefined();
                });
                done();
            }

            getJurisdictions(checkAjaxResponse, checkAjaxResponse);
        }, 10000);
    });
});

describe("Tax category service client", () => {
    describe("GET", () => {
        test("should correctly retrieve tax categories with a 200 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                data.forEach(category => {
                    expect(category.tax_category_id).toBeDefined();
                    expect(category.name).toBeDefined();
                });
                done();
            }

            getTaxCategories(checkAjaxResponse, checkAjaxResponse);
        }, 10000);
    });
});

describe("Form service client", () => {
    describe("GET", () => {
        test("should correctly retrieve the form for the default jurisdiction with id = 1, returning a 200 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.forms).toBeDefined();
                let form = data.forms['1'];
                expect(form).toBeDefined();
                expect(form.id).toBe(1);
                expect(form.jurisdiction_id).toBe(1);
                expect(form.questions).toBeDefined();
                let questions = form.questions;
                questions.forEach(question => {
                    expect(question.text).toBeDefined();
                    expect(question.explainer).toBeDefined();
                    expect(question.ordinal).toBeDefined();
                });
                done();
            }

            getFormForJurisdiction(1, checkAjaxResponse, checkAjaxResponse);
        }, 10000);
    });
});

describe("Question service clients", () => {
    describe("Boolean questions", () => {
        describe("POST", () => {
            test("should correctly create a boolean question, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();

                    done();
                }
    
                let text = "A boolean question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "boolean_var";
                let isMandatory = true;
                createBooleanQuestion(1, text, ordinal, explainer, variableName, isMandatory, checkAjaxResponse, checkAjaxResponse);
            }, 10000);

            test("should correctly return a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Boolean question - invalid test");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(data.status);
                    expect(request).toBeDefined();
                    expect(data.status).toBe(400);
                    expect(data).toBeDefined();
                    expect(data.responseJSON.error).toBeDefined();
                    done();
                }
    
                let text = "A boolean question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = null;
                let isMandatory = true;
                createBooleanQuestion(1, text, ordinal, explainer, variableName, isMandatory, checkAjaxResponse, checkAjaxResponse);
            }, 10000);
        });

        describe("PUT", () => {
            test("should correctly update a boolean question, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking boolean question update results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    done();
                }

                function testUpdateBooleanQuestion(data, textStatus, request) {
                    console.log("Updating boolean question");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();

                    let id = data.id;
                    let text = "A boolean question test - UPDATED";
                    let explainer = "Created by automated test - UPDATED";
                    let ordinal = 2;
                    let variableName = "boolean_var";
                    let isMandatory = true;
                    updateBooleanQuestion(1, id, text, ordinal, explainer, isMandatory, checkAjaxResponse, checkAjaxResponse);
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let text = "A boolean question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "boolean_var";
                let isMandatory = true;
                createBooleanQuestion(1, text, ordinal, explainer, variableName, isMandatory, testUpdateBooleanQuestion, failTest);
            }, 10000);

            test("should fail to update a boolean question, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking boolean question update results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(data.status);
                    expect(request).toBeDefined();
                    expect(data.status).toBe(400);
                    expect(data).toBeDefined();
                    expect(data.responseJSON.error).toBeDefined();
                    done();
                }
    
                function testUpdateBooleanQuestion(data, textStatus, request) {
                    console.log("Updating boolean question");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    let id = data.id;
                    let text = null;
                    let explainer = "Created by automated test - UPDATED";
                    let ordinal = 2;
                    let variableName = null;
                    let isMandatory = true;
                    updateBooleanQuestion(1, id, text, ordinal, explainer, isMandatory, checkAjaxResponse, checkAjaxResponse);
                }
    
                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let text = "A boolean question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "boolean_var";
                let isMandatory = true;
                createBooleanQuestion(1, text, ordinal, explainer, variableName, isMandatory, testUpdateBooleanQuestion, failTest);
            }, 10000);
        });
    });

    describe("Numeric questions", () => {
        describe("POST", () => {
            test("should correctly update numeric question, returning 200 and a valid id", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking create numeric question results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);                    
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    done();
                }
    
                let text = "A numeric question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let isMandatory = true;
                let minValue = 1;
                let maxValue = 100;
                let isInteger = true;
                createNumericQuestion(1, text, ordinal, explainer, variableName, isMandatory, isInteger, minValue, maxValue, checkAjaxResponse, checkAjaxResponse);
            }, 10000);

            test("should fail to create numeric question, returning 400", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking create numeric question results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);
                    expect(data).toBeDefined();
                    expect(data.responseJSON.error).toBeDefined();
                    done();
                }
    
                let text = "A numeric question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = null;
                let isMandatory = true;
                let minValue = null;
                let maxValue = null;
                let isInteger = true;
                createNumericQuestion(1, text, ordinal, explainer, variableName, isMandatory, isInteger, minValue, maxValue, checkAjaxResponse, checkAjaxResponse);
            }, 10000);
        });

        describe("PUT", () => {
            test("should correctly update a boolean question, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking numeric question update results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    done();
                }

                function testUpdateNumericQuestion(data, textStatus, request) {
                    console.log("Updating numeric question");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    let id = data.id;
                    let text = "A numeric question test UPDATED";
                    let explainer = "Created by automated test UPDATED";
                    let ordinal = 1;
                    let variableName = "numeric_var";
                    let isMandatory = true;
                    let minValue = 1;
                    let maxValue = 100;
                    let isInteger = true;
                    updateNumericQuestion(1, id, text, ordinal, explainer, isMandatory, isInteger, minValue, maxValue, checkAjaxResponse, checkAjaxResponse);
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let text = "A numeric question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let isMandatory = true;
                let minValue = 2;
                let maxValue = 60;
                let isInteger = true;
                createNumericQuestion(1, text, ordinal, explainer, variableName, isMandatory, isInteger, minValue, maxValue, testUpdateNumericQuestion, failTest);
            }, 10000);

            test("should fail to update numeric question returning 400 error", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking numeric question update results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data.status).toBe(400);
                    expect(data).toBeDefined();
                    expect(data.responseJSON).toBeDefined();
                    done();
                }

                function testUpdateNumericQuestion(data, textStatus, request) {
                    console.log("Updating numeric question");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    let id = data.id;
                    let text = "A numeric question test UPDATED";
                    let explainer = "Created by automated test UPDATED";
                    let ordinal = null;
                    let variableName = "numeric_var";
                    let isMandatory = true;
                    let minValue = 1;
                    let maxValue = null;
                    let isInteger = true;
                    updateNumericQuestion(1, id, text, ordinal, explainer, isMandatory, isInteger, minValue, maxValue, checkAjaxResponse, checkAjaxResponse);
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let text = "A numeric question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let isMandatory = true;
                let minValue = 2;
                let maxValue = 60;
                let isInteger = true;
                createNumericQuestion(1, text, ordinal, explainer, variableName, isMandatory, isInteger, minValue, maxValue, testUpdateNumericQuestion, failTest);
            }, 10000);
        });
    });

    describe("Multiple choice questions", () => {
        describe("POST", () => {
            test("should correctly create a multiple choice question, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    done();
                }
    
                let text = "A multiple choice test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "multiple_choice_var";
                let isMandatory = true;
                createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, checkAjaxResponse, checkAjaxResponse);
            }, 10000);

            test("should correctly return a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Multiple choice question - invalid test");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(data.status);
                    expect(request).toBeDefined();
                    expect(data.status).toBe(400);
                    expect(data).toBeDefined();
                    expect(data.responseJSON.error).toBeDefined();
                    done();
                }
    
                let text = "A multiple choice question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = null;
                let isMandatory = true;
                createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, checkAjaxResponse, checkAjaxResponse);
            }, 10000);
        });

        describe("PUT", () => {
            test("should correctly update a multiple choice, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking multiple choice update results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    done();
                }

                function testUpdateMultipleChoiceQuestion(data, textStatus, request) {
                    console.log("Updating multiple choice question");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    let id = data.id;
                    let text = "A multiple choice question test - UPDATED";
                    let explainer = "Created by automated test - UPDATED";
                    let ordinal = 2;
                    let isMandatory = true;
                    updateMultipleChoiceQuestion(1, id, text, ordinal, explainer, isMandatory, checkAjaxResponse, checkAjaxResponse);
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let text = "A multiple choice question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "multiple_choice_var";
                let isMandatory = true;
                createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, testUpdateMultipleChoiceQuestion, failTest);
            }, 10000);

            test("should fail to update a multiple choice, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log("Checking multiple choice question update results");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(data.status);
                    expect(request).toBeDefined();
                    expect(data.status).toBe(400);
                    expect(data).toBeDefined();
                    expect(data.responseJSON.error).toBeDefined();
                    done();
                }
    
                function testUpdateMultipleChoiceQuestion(data, textStatus, request) {
                    console.log("Updating multiple choice question");
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.id).toBeDefined();
                    
                    let id = data.id;
                    let text = null;
                    let explainer = "Created by automated test - UPDATED";
                    let ordinal = 2;
                    let variableName = null;
                    let isMandatory = true;
                    updateMultipleChoiceQuestion(1, id, text, ordinal, explainer, isMandatory, checkAjaxResponse, checkAjaxResponse);
                }
    
                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let text = "A multiple choice question test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "multiple_choice_var";
                let isMandatory = true;
                createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, testUpdateMultipleChoiceQuestion, failTest);
            }, 10000);
        });
    });

    describe("DELETE", () => {
        test("should correctly update a multiple choice, returning a 200 response and a valid ID", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log("Checking question deletion results");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                done();
            }

            function testRemoveMultipleChoiceQuestion(data, textStatus, request) {
                console.log("Updating multiple choice question");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.id).toBeDefined();

                removeQuestion(1, data.id, checkAjaxResponse, checkAjaxResponse);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            let text = "A multiple choice question test";
            let explainer = "Created by automated test";
            let ordinal = 1;
            let variableName = "multiple_choice_var";
            let isMandatory = true;
            createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, testRemoveMultipleChoiceQuestion, failTest);
        }, 10000);
    });
});

describe("Multiple choice options", () => {
    describe("POST", () => {
        test("should correctly create a multiple choice option, returning a 200 response and a valid ID", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.option_id).toBeDefined();
                
                done();
            }
            
            function testCreateMultipleChoiceOption(data, textStatus, request) {
                console.log("Creating multiple choice option");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.id).toBeDefined();

                let text = "A test option";
                let explainer = "A wonderful test";

                postMultipleChoiceOption(1, data.id, text, explainer, checkAjaxResponse, checkAjaxResponse);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            let text = "A multiple choice test";
            let explainer = "Created by automated test";
            let ordinal = 1;
            let variableName = "multiple_choice_var";
            let isMandatory = true;
            createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, testCreateMultipleChoiceOption, failTest);
        }, 10000);

        test("should fail to create a multiple choice option, returning a 400 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(data.status).toBe(400);
                expect(data).toBeDefined();
                
                done();
            }
            
            function testCreateMultipleChoiceOption(data, textStatus, request) {
                console.log("Creating multiple choice option");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.id).toBeDefined();

                let text = null;
                let explainer = "A wonderful test";

                postMultipleChoiceOption(1, data.id, text, explainer, checkAjaxResponse, checkAjaxResponse);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            let text = "A multiple choice test";
            let explainer = "Created by automated test";
            let ordinal = 1;
            let variableName = "multiple_choice_var";
            let isMandatory = true;
            createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, testCreateMultipleChoiceOption, failTest);
        }, 10000);
    });

    describe("DELETE", () => {
        test("should correctly delete a multiple choice option, returning a 200 response", done => {
            let questionId = null;
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                
                done();
            }

            function testRemoveMultipleChoiceOption(data, textStatus, request) {
                console.log("Creating multiple choice option");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.option_id).toBeDefined();
                removeMultipleChoiceOption(1, questionId, data.option_id, checkAjaxResponse, checkAjaxResponse);
            }
            
            function testCreateMultipleChoiceOption(data, textStatus, request) {
                console.log("Creating multiple choice option");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.id).toBeDefined();
                questionId = data.id;
                console.log("questionID set to " + questionId);

                let text = "A test option";
                let explainer = "A wonderful test";

                postMultipleChoiceOption(1, data.id, text, explainer, testRemoveMultipleChoiceOption, failTest);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            let text = "A multiple choice test";
            let explainer = "Created by automated test";
            let ordinal = 1;
            let variableName = "multiple_choice_var";
            let isMandatory = true;
            createMultipleChoiceQuestion(1, text, ordinal, explainer, variableName, isMandatory, testCreateMultipleChoiceOption, failTest);
        }, 10000);
    });
});

describe("Ruleset service client", () => {
    describe("POST", () => {
        test("should correctly create a ruleset, returning a 200 response and a valid ID", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.ruleset_id).toBeDefined();

                done();
            }

            postRuleset(1, 1, 1, checkAjaxResponse, checkAjaxResponse);
        }, 10000);

        test("should fail to create a ruleset, returning a 400 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(data).toBeDefined();
                expect(data.status).toBe(400);

                done();
            }

            postRuleset(null, null, 1, checkAjaxResponse, checkAjaxResponse);
        }, 10000);
    });

    describe("PATCH", () => {
        test("should correctly update a ruleset, returning a 200 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);

                done();
            }

            function testUpdateRuleset(data, textStatus, request) {
                console.log("Updating ruleset");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.ruleset_id).toBeDefined();
                
                let id = data.ruleset_id;
                let ordinal = 2;
                patchRuleset(id, ordinal, checkAjaxResponse, checkAjaxResponse);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            postRuleset(2, 1, 1, testUpdateRuleset, failTest);
        }, 10000);

        test("should fail to update a ruleset, returning a 400 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(data.status).toBe(400);

                done();
            }

            function testUpdateRuleset(data, textStatus, request) {
                console.log("Updating ruleset");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.ruleset_id).toBeDefined();
                
                let id = data.ruleset_id;
                let ordinal = null;
                patchRuleset(id, ordinal, checkAjaxResponse, checkAjaxResponse);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            postRuleset(3, 1, 1, testUpdateRuleset, failTest);
        }, 10000);
    });

    describe("DELETE", () => {
        test("should correctly delete a ruleset, returning a 200 response", done => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(data, textStatus, request) {
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);

                done();
            }

            function testRemoveRuleset(data, textStatus, request) {
                console.log("Removing ruleset");
                console.log(data);
                console.log(textStatus);
                console.log(request);
                console.log(request.status);
                expect(request).toBeDefined();
                expect(request.status).toBe(200);
                expect(data).toBeDefined();
                expect(data.ruleset_id).toBeDefined();
                
                let id = data.ruleset_id;
                removeRuleset(id, checkAjaxResponse, checkAjaxResponse);
            }

            function failTest(data, textStatus, request) {
                console.log(data.responseJSON);
                done(data.responseJSON.error);
            }

            postRuleset(4, 1, 1, testRemoveRuleset, failTest);
        }, 10000);
    });
});

describe("Rule service clients", () => {
    beforeAll(done => {
        // Approach to testing asynchronous code adapted from Jest documentation
        // https://jestjs.io/docs/asynchronous
        function checkAjaxResponse(data, textStatus, request) {
            console.log("Ruleset created for use in rule tests")
            console.log(data);
            console.log(textStatus);
            console.log(request);
            console.log(request.status);
            rulesetId = data.ruleset_id;

            done();
        }

        postRuleset(5, 1, 1, checkAjaxResponse, checkAjaxResponse);
    });

    describe("Flat rate rules", () => {
        describe("POST", () => {
            test("should correctly create a flat rate rule, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();

                    done();
                }
    
                let name = "A flat rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let taxRate = 20;
                createFlatRateRule(rulesetId, name, explainer, variableName, ordinal, taxRate, checkAjaxResponse, checkAjaxResponse);
            }, 10000);

            test("should fail to create a flat rate rule, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);

                    done();
                }
    
                let name = null;
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let taxRate = 20;
                createFlatRateRule(rulesetId, name, explainer, variableName, ordinal, taxRate, checkAjaxResponse, checkAjaxResponse);
            }, 10000);
        });

        describe("PUT", () => {
            test("should correctly update a flat rate rule, returning a 200 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();

                    done();
                }

                function testUpdateFlatRateRule(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();

                    let ruleId = data.rule_id;
                    let name = "A flat rate rule test UPDATED";
                    let explainer = "Created by automated test UPDATED";
                    let ordinal = 1;
                    let variableName = "numeric_var";
                    let taxRate = 22;
                    updateFlatRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, taxRate, checkAjaxResponse, checkAjaxResponse);

                    done();
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let name = "A flat rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let taxRate = 20;
                createFlatRateRule(rulesetId, name, explainer, variableName, ordinal, taxRate, testUpdateFlatRateRule, failTest);
            }, 10000);

            test("should fail to update a flat rate rule, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);

                    done();
                }

                function testUpdateFlatRateRule(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();

                    let ruleId = data.rule_id;
                    let name = null;
                    let explainer = "Created by automated test UPDATED";
                    let ordinal = 1;
                    let variableName = "numeric_var";
                    let taxRate = 22;
                    updateFlatRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, taxRate, checkAjaxResponse, checkAjaxResponse);

                    done();
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let name = "A flat rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let taxRate = 20;
                createFlatRateRule(rulesetId, name, explainer, variableName, ordinal, taxRate, testUpdateFlatRateRule, failTest);
            }, 10000);
        });
    });

    describe("Tiered rate rules", () => {
        describe("POST", () => {
            test("should correctly create a tiered rate rule, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();
                    tieredRateRuleId = data.rule_id;
                    done();
                }
    
                let name = "A tiered rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, checkAjaxResponse, checkAjaxResponse);
            }, 10000);

            test("should fail to create a tiered rate rule, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);

                    done();
                }
    
                let name = null;
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                let taxRate = 20;
                createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, checkAjaxResponse, checkAjaxResponse);
            }, 10000);
        });

        describe("PUT", () => {
            test("should correctly update a tiered rate rule, returning a 200 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();

                    done();
                }

                function testUpdateTieredRateRule(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();

                    let ruleId = data.rule_id;
                    let name = "A tiered rate rule test UPDATED";
                    let explainer = "Created by automated test UPDATED";
                    let ordinal = 1;
                    let variableName = "numeric_var";
                    updateTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, checkAjaxResponse, checkAjaxResponse)

                    done();
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let name = "A flat rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, testUpdateTieredRateRule, failTest);
            }, 10000);

            test("should fail to update a tiered rate rule, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);

                    done();
                }

                function testUpdateTieredRateRule(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();

                    let ruleId = data.rule_id;
                    let name = null;
                    let explainer = "Created by automated test UPDATED";
                    let ordinal = 1;
                    let variableName = "numeric_var";
                    updateTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, checkAjaxResponse, checkAjaxResponse)

                    done();
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let name = "A flat rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createTieredRateRule(rulesetId, name, explainer, variableName, ordinal, testUpdateTieredRateRule, failTest);
            }, 10000);
        });
    });

    describe("Secondary tiered rate rules", () => {
        describe("POST", () => {
            test("should correctly create a secondary tiered rate rule, returning a 200 response and a valid ID", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();
                    done();
                }
    
                let name = "A secondary tiered rate rule test";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, tieredRateRuleId, checkAjaxResponse, checkAjaxResponse);
            }, 10000);

            test("should fail to create a secondary tiered rate rule, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);

                    done();
                }
    
                let name = null;
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, tieredRateRuleId, checkAjaxResponse, checkAjaxResponse);
            }, 10000);
        });

        describe("PUT", () => {
            test("should correctly update a secondary tiered rate rule, returning a 200 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();

                    done();
                }

                function testUpdateSecondaryTieredRateRule(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();
                    expect(data.rule_id).toBeDefined();

                    let ruleId = data.rule_id;
                    let name = "Secondary tiered rate rule UPDATED";
                    let explainer = "Created by automated test";
                    let ordinal = 2;
                    let variableName = "numeric_var";
                    updateSecondaryTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, tieredRateRuleId, checkAjaxResponse, checkAjaxResponse);

                    done();
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let name = "Secondary tiered rate rule";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, tieredRateRuleId, testUpdateSecondaryTieredRateRule, failTest);
            }, 10000);

            test("should fail to update a secondary tiered rate rule, returning a 400 response", done => {
                // Approach to testing asynchronous code adapted from Jest documentation
                // https://jestjs.io/docs/asynchronous
                function checkAjaxResponse(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);
                    expect(data).toBeDefined();
                    expect(data.status).toBe(400);

                    done();
                }

                function testUpdateSecondaryTieredRateRule(data, textStatus, request) {
                    console.log(data);
                    console.log(textStatus);
                    console.log(request);
                    console.log(request.status);

                    expect(request).toBeDefined();
                    expect(request.status).toBe(200);
                    expect(data).toBeDefined();

                    let ruleId = data.rule_id;
                    let name = null;
                    let explainer = "Created by automated test";
                    let ordinal = 1;
                    let variableName = "numeric_var";
                    updateSecondaryTieredRateRule(rulesetId, ruleId, name, explainer, variableName, ordinal, tieredRateRuleId, checkAjaxResponse, checkAjaxResponse);

                    done();
                }

                function failTest(data, textStatus, request) {
                    console.log(data.responseJSON);
                    done(data.responseJSON.error);
                }
    
                let name = "Secondary tiered rate rule";
                let explainer = "Created by automated test";
                let ordinal = 1;
                let variableName = "numeric_var";
                createSecondaryTieredRateRule(rulesetId, name, explainer, variableName, ordinal, tieredRateRuleId, testUpdateSecondaryTieredRateRule, failTest);
            }, 10000);
        });
    });

    describe("DELETE", () => {

    });
});

describe("Rule tier service clients", () => {
    describe("Primary rule tiers", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

        });

        describe("DELETE", () => {

        });
    });

    describe("Secondary rule tiers", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

        });

        describe("DELETE", () => {

        });
    });
});