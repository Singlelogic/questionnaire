from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .models import Answer, Question, Questionnaire
from .serializers import AnswerSerializer, QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        question = get_object_or_404(Question, id=self.request.data.get('question_id'))
        return serializer.save(question=question)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        question = get_object_or_404(Questionnaire, id=self.request.data.get('questionnaire_id'))
        return serializer.save(question=question)
