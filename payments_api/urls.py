from django.urls import path
from .views import *

urlpatterns = [
    path('', PaymentsList.as_view()),
    path('<int:pk>/', PaymentDetail.as_view()),
    path('<int:pk>/status/', PaymentStatusDetail.as_view()),
    path('webhooks/', StripeWebhooksList.as_view()),
]