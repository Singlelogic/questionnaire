from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AnswerViewSet, AnswerUserViewSet, QuestionViewSet, QuestionnaireViewSet
)

urlpatterns = [
    path("questionnaire/active/",
         QuestionnaireViewSet.as_view({'get': 'active'}, name='questionnaire_active')),
    path("get_user_responses/<pk>/",
         AnswerUserViewSet.as_view({'get': 'get_user_responses'}, name='get_user_responses'))
]

router = DefaultRouter()
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')
router.register(r'answer_user', AnswerUserViewSet, basename='answer_user')

urlpatterns.extend(router.urls)
