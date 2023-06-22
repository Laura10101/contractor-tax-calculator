from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('confirm/', views.confirm_checkout, name='confirm_checkout'),
    path('status/<int:id>/', views.checkout_status, name='checkout_status'),
]