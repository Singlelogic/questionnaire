from collections import defaultdict
from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Answer, AnsewrUser, Question, Questionnaire
from .permissions import IsAdminOrReadOnly
from .serializers import (
    AnswerSerializer, AnswerUserSerializer, QuestionSerializer,
    QuestionnaireSerializer,
)


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
    """This class represents questions.

    Allows administrators to create, edit and delete questions.
    All users can get questions and options for answers to these questions.
    """
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs):
        """Method for creating questions.

        If the questionnaire has a start date for the survey,
        it is prohibited to add new questions.
        """
        if request.data.get('questionnaire_id'):
            questionnaire = Questionnaire.objects.get(id=request.data['questionnaire_id'])
            if not questionnaire.date_start:
                return super().create(request, *args, **kwargs)
            return Response({
                "message": "After specifying the start date of the survey, "
                           "you cannot create new questions."
            }, status=403)
        return Response({
            "message": "No 'questionnaire_id' specified."
        }, status=406)

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
            "message": "After specifying the start date for the survey, "
                       "you cannot change the questions."
        }, status=403)

    def destroy(self, request, *args, **kwargs):
        """Method for removing questions.

        If the date of the start of the survey is indicated in the questionnaire,
        deleting questions is prohibited.
        """
        if not self.get_object().questionnaire.date_start:
            return super().destroy(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date of the survey, "
                       "you cannot delete questions."
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
        if request.data.get('question_id'):
            question = Question.objects.get(id=request.data['question_id'])
            if not question.questionnaire.date_start:
                if question.type > 1:
                    return super().create(request, *args, **kwargs)
                return Response({
                    "message": "This type of question requires a text answer."
                }, status=406)
            return Response({
                "message": "After specifying the start date of the survey, "
                           "you cannot create new answers."
            }, status=403)
        return Response({
            "message": "No 'question_id' specified."
        }, status=406)

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
            "message": "After specifying the start date for the survey, "
                       "you cannot change the answers."
        }, status=403)

    def destroy(self, request, *args, **kwargs):
        """Method for removing answers.

        If the date of the start of the survey is indicated in the questionnaire,
        deleting questions is prohibited.
        """
        if not self.get_object().question.questionnaire.date_start:
            return super().destroy(request, *args, **kwargs)
        return Response({
            "message": "After specifying the start date of the survey, "
                       "you cannot delete answers."
        }, status=403)


class AnswerUserViewSet(viewsets.ModelViewSet):
    """This class contains user responses to questions."""
    serializer_class = AnswerUserSerializer
    queryset = AnsewrUser.objects.all()

    def create(self, request, *args, **kwargs):
        """Method for creating answer for questions."""
        if request.data.get('question'):
            question = Question.objects.get(id=request.data['question'])
            type_question = question.type
            message = self._is_valid_answer(request, type_question)
            if not message:
                return super().create(request, *args, **kwargs)
            return Response({
                "message": f"{message}"
            }, status=403)
        return Response({
            "message": "No 'question' specified."
        }, status=406)

    @staticmethod
    def _is_valid_answer(request, type_question):
        """Checking the user's response.

        It checks whether the user has ever answered this question and,
        if he did not answer, whether the answer matches the type of question.
        Question types:
        1. Reply in text
        2. Answer with a choice of one option
        3. Multiple choice answer
        """
        user_id = request.data.get('user_id')
        question_id = request.data.get('question')
        is_already_answer = AnsewrUser.objects.filter(
            user_id=user_id).filter(question_id=question_id)

        if is_already_answer:
            return "The user already has an answer to this question."
        elif request.data.get('text_answer') and request.data.get('choice_answer'):
            return "It is forbidden to answer simultaneously " \
                   "with the text and the choice of answers."
        elif request.data.get('text_answer') and type_question in (2, 3):
            return "There should be no textual response."
        elif request.data.get('choice_answer') and type_question == 1:
            return "The answer must be text."
        elif request.data.get('choice_answer'):
            if len(request.data.get('choice_answer')) > 1 and type_question == 2:
                return "This question requires only one answer option."
        elif not request.data.get('text_answer') and not request.data.get('choice_answer'):
            return "The question must be answered."

    @action(detail=True)
    def get_user_responses(self, request, pk=None):
        """Retrieve user responses to survey questions."""
        answers = AnsewrUser.objects.filter(user_id=pk)

        result = defaultdict(dict)

        for answer in answers:
            answer_s = str(answer)
            question_s = str(answer.question)
            questionnaire_s = str(answer.question.questionnaire)

            if result[questionnaire_s].get(question_s):
                result[questionnaire_s][question_s].append(answer_s)
            else:
                result[questionnaire_s][question_s] = [answer_s]

        return Response(result)
