from datetime import date

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Answer, Question, Questionnaire
from .serializers import AnswerSerializer, QuestionSerializer, QuestionnaireSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """This is a answer view class that you can use to create, modify, or delete answers."""
    # permission_classes = (IsAdminUser,)
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


class QuestionViewSet(viewsets.ModelViewSet):
    """This is a question viewer class with which you can create, modify or delete questions."""
    permission_classes = (IsAdminUser,)
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


class QuestionnaireViewSet(viewsets.ModelViewSet):
    """This is a question viewer class with which you can create, modify or delete questions."""
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()


class QuestionnaireActive(viewsets.ReadOnlyModelViewSet):
    """This view class to get all active polls."""
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.filter(
        date_start__lte=date.today()).filter(
        date_stop__gte=date.today())
