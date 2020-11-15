from rest_framework.routers import DefaultRouter

from .views import AnswerViewSet, QuestionViewSet, QuestionnaireViewSet


router = DefaultRouter()
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')

urlpatterns = router.urls
