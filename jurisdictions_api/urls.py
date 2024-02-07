"""Define urls for the jurisdictions API."""

from django.urls import path, re_path
from .autocompletes import JurisdictionAutocomplete
from .views import JurisdictionList

urlpatterns = [
    path('', JurisdictionList.as_view(), name='jurisdictions'),
    re_path(
        r'^jurisdiction-autocomplete/$',
        JurisdictionAutocomplete.as_view(),
        name='jurisdiction-autocomplete',
    ),
]
