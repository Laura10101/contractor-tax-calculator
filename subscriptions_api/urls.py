from django.urls import path, re_path
from .autocompletes import SubscriptionAutocomplete, SubscriptionOptionAutocomplete
from .views import *

urlpatterns = [
    path('', SubscriptionsList.as_view()),
    path('<int:pk>/', SubscriptionDetail.as_view()),
    path('status/', SubscriptionStatusesList.as_view()),
    path('options/', SubscriptionOptionsList.as_view()),
    path('options/<int:pk>', SubscriptionOptionDetail.as_view()),
    re_path(
        r'^subscription-autocomplete/$',
        SubscriptionAutocompleteAutocomplete.as_view(),
        name='subscription-autocomplete',
    ),
    re_path(
        r'^subscription-option-autocomplete/$',
        SubscriptionOptionAutocompleteAutocomplete.as_view(),
        name='subscription-option-autocomplete',
    ),
]