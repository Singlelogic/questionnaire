from django.test import TestCase

from questionnaire_api.models import Questionnaire


class QuestionnaireModelTest(TestCase):
    """
    Test class for Questionnaire
    """
    @classmethod
    def setUpTestData(cls):
        Questionnaire.objects.create(
            title='Weather',
            description='What kind of weather do you like?',
            date_start='2020-11-23',
            date_stop='2020-11-23'
        )

    def test_title_lable(self):
        quistionnaire = Questionnaire.objects.get(id=1)
        field_label = quistionnaire._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_lable(self):
        quistionnaire = Questionnaire.objects.get(id=1)
        field_label = quistionnaire._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_date_start_lable(self):
        quistionnaire = Questionnaire.objects.get(id=1)
        field_label = quistionnaire._meta.get_field('date_start').verbose_name
        self.assertEqual(field_label, 'date start')

    def test_date_stop_lable(self):
        quistionnaire = Questionnaire.objects.get(id=1)
        field_label = quistionnaire._meta.get_field('date_stop').verbose_name
        self.assertEqual(field_label, 'date stop')

    def test_title_max_lenght(self):
        questionnaire = Questionnaire.objects.get(id=1)
        max_length = questionnaire._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_description(self):
        questionnaire = Questionnaire.objects.get(id=1)
        expected_object_name = questionnaire.description
        self.assertEqual(expected_object_name, str(questionnaire))
