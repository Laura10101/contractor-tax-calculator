from django.urls import path
from . import views

urlpatterns = [
    path('jurisdictions/select', views.select_jurisdictions, name='select_jurisdictions'),
]