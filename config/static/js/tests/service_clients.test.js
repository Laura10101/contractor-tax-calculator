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

        });
    });

    describe("Numeric questions", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

        });
    });

    describe("Multiple choice questions", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

        });
    });

    describe("DELETE", () => {

    });
});

describe("Ruleset service client", () => {
    describe("POST", () => {

    });

    describe("PATCH", () => {

    });

    describe("DELETE", () => {

    });
});

describe("Rule service clients", () => {
    describe("Flat rate rules", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

        });
    });

    describe("Tiered rate rules", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

        });
    });

    describe("Secondary tiered rate rules", () => {
        describe("POST", () => {

        });

        describe("PUT", () => {

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