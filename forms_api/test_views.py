from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import *
from .services import *
from .views import *
import pytest

client = APIClient()
url = '/api/jurisdictions/'

# Create your tests here.
# Test creation of jurisdictions
@pytest.mark.django_db