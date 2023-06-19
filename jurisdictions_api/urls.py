from django.urls import path
from .views import *

urlpatterns = [
    path('', JurisdictionList.as_view(), name='jurisdictions'),
]