from rest_framework.routers import DefaultRouter

from .views import (
    AnswerViewSet, QuestionViewSet, QuestionnaireViewSet, QuestionnaireActive
)

router = DefaultRouter()
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')
router.register(r'questionnaire_active', QuestionnaireActive, basename='questionnaire_active')

urlpatterns = router.urls
