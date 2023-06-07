from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest

# Test creating a subscription
@pytest.mark.django_db