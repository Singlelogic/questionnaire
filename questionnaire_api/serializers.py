from rest_framework import serializers

from .models import Answer, Question, Questionnaire


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'type', 'questionnaire_id')


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'description', 'date_start', 'date_stop', 'is_active')
