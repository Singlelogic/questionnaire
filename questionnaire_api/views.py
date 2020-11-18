from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Answer, Question, Questionnaire
from .permissions import IsAdminOrReadOnly
from .serializers import AnswerSerializer, QuestionSerializer, QuestionnaireSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    """This class contains polls.

    Allows admins to create, edit and delete polls and receive all polls.
    Methods are available for anonymous users to get all active polls and
    get questions in polls.
    """
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()

    @staticmethod
    def active(self):
        """This method only represents active polls."""
        questionnaire = Questionnaire.objects.filter(
            date_start__lte=date.today()).filter(
            date_stop__gte=date.today())
        serializer = QuestionnaireSerializer(questionnaire, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def questions(self, request, pk=None):
        """This method for getting questions on a specific survey."""
        questionnaire = Questionnaire.objects.get(pk=pk)
        questions = Question.objects.filter(questionnaire=questionnaire)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    """This is a question viewer class with which you can create, modify or delete questions."""
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs):
        """Method for creating questions.

        If the questionnaire has a start date for the survey, it is prohibited to add new questions.
        """
        questionnaire = Questionnaire.objects.get(id=request.data['questionnaire_id'])
        if not questionnaire.date_start:
            return super().create(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date of the survey, you cannot create new questions."
        }, status=403)

    def perform_create(self, serializer):
        obj = get_object_or_404(Questionnaire, id=self.request.data.get('questionnaire_id'))
        return serializer.save(questionnaire=obj)

    def update(self, request, *args, **kwargs):
        """Method for changing questions.

        If the date of the start of the survey is indicated in the questionnaire,
        it is prohibited to change the questions.
        """
        if not self.get_object().questionnaire.date_start:
            return super().update(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date for the survey, you cannot change the questions."
        }, status=403)

    def destroy(self, request, *args, **kwargs):
        """Method for removing questions.

        If the date of the start of the survey is indicated in the questionnaire,
        deleting questions is prohibited.
        """
        if not self.get_object().questionnaire.date_start:
            return super().destroy(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date of the survey, you cannot delete questions."
        }, status=403)

    @action(detail=True)
    def answers(self, request, pk=None):
        """This method for getting answers on a specific question."""
        question = Question.objects.get(pk=pk)
        answers = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    """This is a answer view class that you can use to create, modify, or delete answers."""
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def create(self, request, *args, **kwargs):
        """Method for creating answers.

        If the questionnaire has a start date for the survey, it is prohibited to add new answers.
        """
        question = Question.objects.get(id=request.data['question_id'])
        if not question.questionnaire.date_start:
            return super().create(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date of the survey, you cannot create new answers."
        }, status=403)

    def perform_create(self, serializer):
        obj = get_object_or_404(Question, id=self.request.data.get('question_id'))
        return serializer.save(question=obj)

    def update(self, request, *args, **kwargs):
        """Method for changing answers.

        If the date of the start of the survey is indicated in the questionnaire,
        it is prohibited to change the answers.
        """
        if not self.get_object().question.questionnaire.date_start:
            return super().update(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date for the survey, you cannot change the answers."
        }, status=403)

    def destroy(self, request, *args, **kwargs):
        """Method for removing answers.

        If the date of the start of the survey is indicated in the questionnaire,
        deleting questions is prohibited.
        """
        if not self.get_object().question.questionnaire.date_start:
            return super().destroy(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date of the survey, you cannot delete answers."
        }, status=403)
