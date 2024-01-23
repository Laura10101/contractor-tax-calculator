#!/usr/bin/env python
import os
import sys

# Delete the existing SQL Lite DB
# Taken from W3 Schools
# https://www.w3schools.com/python/python_file_remove.asp
fn = "db.sqlite3"
if os.path.exists(fn):
    print("Database file exists. Removing it...")
    os.remove(fn)
    print("Removed.")
else:
    print("The database file does not exist")

# Use Django in Standalone mode
# https://docs.djangoproject.com/en/5.0/topics/settings/
print("Specifying settings module")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contractor_tax_calculator.settings')

print("Setting up Django in standalone mode")
import django
django.setup()

# Run migrations
print("Running Django migrations")
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'migrate'])
print("Migrated")

# Setup test data
print("Setting up test data - jurisdictions")
from jurisdictions_api.services import create_jurisdiction
jurisdiction_id = create_jurisdiction("Test Jurisdiction")
print("Created jurisdiction with id = " + str(jurisdiction_id))

print("Setting up test data - form for jurisdiction")
from forms_api.services import create_form
form_id = create_form(jurisdiction_id)
print("Created form with id = " + str(form_id))

print("Setting up test data - tax categories")
from rules_api.services import create_tax_category
names = ['Income Tax', 'Dividend Tax', 'Corporation Tax', 'VAT']
for name in names:
    tax_category_id = create_tax_category(name)
    print('Created tax cateogry with name=' + name + ' and id=' + str(tax_category_id))

print("Ready to go")