from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest


# Create your tests here.
# Test creation of jurisdictions
@pytest.mark.django_db