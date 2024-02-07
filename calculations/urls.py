"""Define urls for the calculations app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_calculation, name='display_calculation'),
    path(
        'jurisdictions/select',
        views.select_jurisdictions,
        name='select_jurisdictions'
    ),
    path('form', views.display_form, name='display_form'),
]
