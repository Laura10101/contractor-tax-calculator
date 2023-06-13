from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('status/', views.checkout_status, name='checkout_status')
]