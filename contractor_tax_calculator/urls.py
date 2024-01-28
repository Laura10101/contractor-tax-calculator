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
from django.urls import path, include, re_path
from home.views import *
from jurisdictions_api.views import JurisdictionList
from forms_api.views import FormDetail, FormsList, FormQuestionList, FormQuestionsDetail
from rules_api.views import *
from subscriptions_api.views import *
from payments_api.views import *


urlpatterns = [
    # Landing pages for all users, contractors, and admin users
    path('', index, name='index'),
    path('contractors/home/', home, name='contractor_home'),
    path('contractors/', contractor_index, name='contractor_index'),
    path('admin/', admin_index, name='admin_index'),

    # All Auth
    path('accounts/', include('allauth.urls')),

    # Admin apps
    path('admin/manage/config/', include('config.urls')),
    path('admin/manage/', admin.site.urls, name='admin'),

    # Contractor apps
    path('contractors/checkout/', include('checkout.urls')),
    path('contractors/subscription/', include('subscription.urls')),
    path('contractors/calculations/', include('calculations.urls')),

    # APIs
    path('api/jurisdictions/', include('jurisdictions_api.urls')),
    path('api/subscriptions/', include('subscriptions_api.urls')),
    path('api/payments/', include('payments_api.urls')),
    path('api/forms/', include('forms_api.urls')),
    path('api/rules/', include('rules_api.urls')),
]
