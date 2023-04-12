from django.shortcuts import render
from .services import get_all_jurisdictions

# Create your views here.
# Create the controller method to retrieve jurisdictions
def get_jurisdictions():
    jurisdictions = get_all_jurisdictions()
    response = { 'jurisdictions' : jurisdictions }
    return HttpResponse(response)