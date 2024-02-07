"""Set up the test database prior to running Jest tests."""
import os
import django
from django.core.management import execute_from_command_line


def setup():
    """Setup the clean test database"""
    # Delete the existing SQL Lite DB
    # Taken from W3 Schools
    # https://www.w3schools.com/python/python_file_remove.asp
    FN = "db.sqlite3"
    if os.path.exists(FN):
        print("Database file exists. Removing it...")
        os.remove(FN)
        print("Removed.")
    else:
        print("The database file does not exist")

    # Use Django in Standalone mode
    # https://docs.djangoproject.com/en/5.0/topics/settings/
    print("Specifying settings module")
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'contractor_tax_calculator.settings'
    )

    print("Setting up Django in standalone mode")
    django.setup()

    # Run migrations
    print("Running Django migrations")
    execute_from_command_line(['manage.py', 'migrate'])
    print("Migrated")

setup()