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
            expect(url).toBe("http://" + window.location.hostname + "/api/test/");
        });
    });
});

describe("Jurisdiction service client", () => {
    describe("GET", () => {
        test("should correctly retrieve jurisdictions with a 200 response", () => {
            // Approach to testing asynchronous code adapted from Jest documentation
            // https://jestjs.io/docs/asynchronous
            function checkAjaxResponse(request, status, message) {
                expect(status).toBe(200);
                expect(request.data).toBeDefined();
                let data = request.data;
                expect(data.questions).tobBeDefined();
                done();
            }

            getJurisdictions(checkAjaxResponse, checkAjaxResponse);
        });
    });
});

describe("Tax category service client", () => {
    describe("GET", () => {

    });
});

describe("Form service client", () => {
    describe("GET", () => {

    });
});

describe("Question service clients", () => {
    describe("Boolean questions", () => {
        describe("POST", () => {

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