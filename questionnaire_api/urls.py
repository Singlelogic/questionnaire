from rest_framework.routers import DefaultRouter

from .views import AnswerViewSet, QuestionViewSet


router = DefaultRouter()
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'question', QuestionViewSet, basename='question')

urlpatterns = router.urls
