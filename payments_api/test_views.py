from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import *
from .services import *
from .views import *
import pytest

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest

client = APIClient()
url = '/api/subscriptions/'

# Test creating a subscription
@pytest.mark.django_db