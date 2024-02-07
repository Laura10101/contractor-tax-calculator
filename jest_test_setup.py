"""Set up the test database prior to running Jest tests."""
import django_test_setup
from jurisdictions_api.services import create_jurisdiction
from rules_api.services import create_tax_category

# Setup test data
print("Setting up test data - jurisdictions")
jurisdiction_id = create_jurisdiction("Test Jurisdiction")
print("Created jurisdiction with id = " + str(jurisdiction_id))

print("Setting up test data - tax categories")
names = ['Income Tax', 'Dividend Tax', 'Corporation Tax', 'VAT']
for name in names:
    tax_category_id = create_tax_category(name)
    print('Created tax cateogry ' + name + ' and id=' + str(tax_category_id))

print("Ready to go")
