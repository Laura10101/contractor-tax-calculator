"""Define urls for the forms API."""
from django.urls import path
from .views import (
    MultipleChoiceOptionDetail,
    MultipleChoiceOptionsList,
    FormQuestionList,
    FormQuestionsDetail,
    FormsList
)

urlpatterns = [
    path(
        '<int:form_pk>/questions/<int:question_pk>/options/<int:pk>/',
        MultipleChoiceOptionDetail.as_view()
    ),
    path(
        '<int:form_pk>/questions/<int:question_pk>/options/',
        MultipleChoiceOptionsList.as_view()
    ),
    path('<int:form_pk>/questions/<int:pk>/', FormQuestionsDetail.as_view()),
    path('<int:form_pk>/questions/', FormQuestionList.as_view()),
    path('', FormsList.as_view(), name='forms'),
]
