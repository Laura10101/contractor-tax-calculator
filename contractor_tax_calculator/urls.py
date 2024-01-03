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
from jurisdictions_api.views import JurisdictionList
from forms_api.views import FormDetail, FormsList, FormQuestionList, FormQuestionsDetail
from rules_api.views import *
from subscriptions_api.views import *
from payments_api.views import *


urlpatterns = [
    path('admin/config/', include('config.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('api/jurisdictions/', include('jurisdictions_api.urls')),
    path('api/subscriptions/', include('subscriptions_api.urls')),
    path('api/payments/', include('payments_api.urls')),
    path('api/forms/', include('forms_api.urls')),
    path('api/rules/', include('rules_api.urls')),
    path('accounts/', include('allauth.urls')),
    path('checkout/', include('checkout.urls')),
    path('', include('home.urls')),
    path('subscription/', include('subscription.urls')),
    path('calculations/', include('calculations.urls'))
]
