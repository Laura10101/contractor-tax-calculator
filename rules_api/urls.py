from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('rulesets/<int:ruleset_pk>/rules/<int:rule_pk>/tiers/', RuleTiersList.as_view()),
    path('rulesets/<int:ruleset_pk>/rules/<int:rule_pk>/tiers/<int:pk>/', RuleTierDetail.as_view()),
    path('rulesets/<int:ruleset_pk>/rules/<int:rule_pk>/secondarytiers/', SecondaryRuleTiersList.as_view()),
    path('rulesets/<int:ruleset_pk>/rules/<int:rule_pk>/secondarytiers/<int:pk>/', SecondaryRuleTierDetail.as_view()),
    path('rulesets/', RuleSetsList.as_view()),
    path('rulesets/<int:pk>/', RuleSetDetail.as_view()),
    path('rulesets/<int:ruleset_pk>/rules/', RuleList.as_view()),
    path('rulesets/<int:ruleset_pk>/rules/<int:pk>/', RuleDetail.as_view()),
    path('taxcategories/', TaxCategoriesList.as_view()),
    path('taxcategories/<int:pk>/', TaxCategoryDetail.as_view()),
]