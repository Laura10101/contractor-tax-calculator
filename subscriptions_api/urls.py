"""Define urls for the subscription API."""
from django.urls import path, re_path
from .autocompletes import (
    SubscriptionAutocomplete,
    SubscriptionOptionAutocomplete,
    UserAutocomplete
)
from .views import *

urlpatterns = [
    path('', SubscriptionsList.as_view()),
    path('status/', SubscriptionStatusesList.as_view()),
    path('options/', SubscriptionOptionsList.as_view()),
    path('options/<int:pk>', SubscriptionOptionDetail.as_view()),
    re_path(
        r'^subscription-autocomplete/$',
        SubscriptionAutocomplete.as_view(),
        name='subscription-autocomplete',
    ),
    re_path(
        r'^subscription-option-autocomplete/$',
        SubscriptionOptionAutocomplete.as_view(),
        name='subscription-option-autocomplete',
    ),
    re_path(
        r'^user-autocomplete/$',
        UserAutocomplete.as_view(),
        name='user-autocomplete',
    ),
]
