"""contractor_tax_calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from jurisdictions_api.views import JurisdictionList
from forms_api.views import FormDetail, FormsList, FormQuestionList, FormQuestionsDetail
from rules_api.views import *
from subscriptions_api.views import *
from payments_api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/jurisdictions/', JurisdictionList.as_view()),
    path('api/forms/', FormsList.as_view()),
    path('api/forms/<int:pk>/', FormDetail.as_view()),
    path('api/forms/<int:form_pk>/questions/', FormQuestionList.as_view()),
    path('api/forms/<int:form_pk>/questions/<int:pk>/', FormQuestionsDetail.as_view()),
    path('api/rulesets/', RuleSetsList.as_view()),
    path('api/rulesets/<int:pk>/', RuleSetDetail.as_view()),
    path('api/taxcategories/', TaxCategoriesList.as_view()),
    path('api/taxcategories/<int:pk>/', TaxCategoryDetail.as_view()),
    path('api/rules/', RuleList.as_view()),
    path('api/rules/<int:pk>/', RuleDetail.as_view()),
    path('api/rules/<int:rule_pk>/tiers/', RuleTiersList.as_view()),
    path('api/rules/<int:rule_pk>/tiers/<int:pk>/', RuleTierDetail.as_view()),
    path('api/rules/<int:rule_pk>/secondarytiers/', SecondaryRuleTiersList.as_view()),
    path('api/rules/<int:rule_pk>/secondarytiers/<int:pk>/', SecondaryRuleTierDetail.as_view()),
    path('api/subscriptions/', SubscriptionsList.as_view()),
    path('api/subscriptions/<int:pk>/', SubscriptionDetail.as_view()),
    path('api/subscriptions/status/', SubscriptionStatusesList.as_view()),
    path('api/subscriptions/options/', SubscriptionOptionsList.as_view()),
    path('api/subscriptions/options/<int:pk>', SubscriptionOptionDetail.as_view()),
    path('api/payments/', PaymentsList.as_view()),
    path('api/payments/<int:pk>/', PaymentDetail.as_view()),
    path('api/payments/<int:pk>/status/', PaymentStatusDetail.as_view()),
    path('api/payments/webhooks/', StripeWebhooksList.as_view()),
    path('accounts/', include('allauth.urls')),
    path('checkout/', include('checkout.urls')),
    path('home/', include('home.urls')),
    path('subscription/', include('subscription.urls')),
]
