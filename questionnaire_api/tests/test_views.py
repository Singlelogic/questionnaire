import json
from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from authentication.models import User
from questionnaire_api.models import (
    Questionnaire
)


class QuestionnaireViewSetViewTest(TestCase):
    """
    Test fot view class QuestionnaireViewSet
    """
    fixtures = ['initial_data.json']

    def test_active(self):
        """
        Check if the poll is active.

        An active poll is a poll with a start date less than or equal to the
        current day and an end date greater than or equal to the current day.
        Polls without start and end dates are considered inactive.
        """
        yesterday = date.today() - timedelta(days=1)
        today = date.today()
        tomorrow = date.today() + timedelta(days=1)

        weather = Questionnaire.objects.get(id=1)
        weather.date_start = yesterday
        weather.date_stop = yesterday
        weather.save()

        clothes = Questionnaire.objects.get(id=2)
        clothes.date_start = today
        clothes.date_stop = today
        clothes.save()

        games = Questionnaire.objects.get(id=3)
        games.date_start = tomorrow
        games.date_stop = tomorrow
        games.save()

        today_b = bytes(str(today), 'utf-8')
        expected = b'[{"id":2,"title":"Clothes","description":"Clothes questionnaire.","date_start":"' + \
                  today_b + b'","date_stop":"' + today_b + b'"}]'

        resp = self.client.get(reverse('questionnaire_active'))
        self.assertEqual(resp.content, expected)

    def test_questions(self):
        """
        Compliance of questions with polls is checked.
        """
        expected_list = [
            b'[{"id":1,"question":"What kind of weather do you like?","type":1,'
            b'"questionnaire_id":1},{"id":2,"question":"Do you like warm weather?",'
            b'"type":1,"questionnaire_id":1}]',
            b'[{"id":3,"question":"What kind of clothes do you like?",'
            b'"type":2,"questionnaire_id":2}]',
            b'[{"id":4,"question":"What kind of games do you like?","type":3,'
            b'"questionnaire_id":3}]',
            b'[{"id":5,"question":"What kind of animals do you like?","type":3,'
            b'"questionnaire_id":4},{"id":6,"question":"Do you like dogs?",'
            b'"type":1,"questionnaire_id":4}]'
        ]

        for i, expected in enumerate(expected_list, start=1):
            resp = self.client.get(reverse('questionnaire-questions', kwargs={'pk': i}))
            self.assertEqual(resp.content, expected)


class QuestionViewSetTest(TestCase):
    """
    Test fot view class QuestionViewSet
    """
    fixtures = ['initial_data.json']

    @classmethod
    def setUpTestData(cls):
        """Create superuser."""
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='12345678')

    @staticmethod
    def active_survey() -> None:
        """Setting active polling."""
        today = date.today()

        animals = Questionnaire.objects.get(id=4)
        animals.date_start = today
        animals.date_stop = today
        animals.save()

    def get_token(self):
        """Getting a token."""
        resp = self.client.post(reverse('user_login'), {
            'email': 'admin@gmail.com', 'password': '12345678'
        })

        token = resp.data['token']
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + token}

        return auth_headers

    def test_create_is_not_admin(self):
        """Check the prohibition of creating questions by a non-administrator."""
        resp = self.client.post(reverse('question-list'))

        expected = b'{"detail":"Authentication credentials were not provided."}'
        self.assertEqual(resp.content, expected)

    def test_create_as_admin(self):
        """Creation of questions by the administrator."""
        auth_headers = self.get_token()
        resp = self.client.post(reverse('question-list'), {
            'questionnaire_id': 1,
            'question': 'test',
            'type': 1
        }, **auth_headers)

        expected = b'{"id":7,"question":"test","type":1,"questionnaire_id":1}'
        self.assertEqual(resp.content, expected)

    def test_create_without_questionnaire_id(self):
        """Creation of questions by the administrator without 'questionnaire_id'."""
        auth_headers = self.get_token()
        resp = self.client.post(reverse('question-list'), {
            'question': 'test',
            'type': 1
        }, **auth_headers)

        expected = b'{"message":"No \'questionnaire_id\' specified."}'
        self.assertEqual(resp.content, expected)

    def test_create_active_survey(self):
        """Create a question for an active survey with administrator rights."""
        self.active_survey()

        auth_headers = self.get_token()
        resp = self.client.post(reverse('question-list'), {
            'questionnaire_id': 4,
            'question': 'test',
            'type': 1
        }, **auth_headers)

        expected = b'{"message":"After specifying the start date ' \
                   b'of the survey, you cannot create new questions."}'
        self.assertEqual(resp.content, expected)

    def test_update_is_not_admin(self):
        """Check the ban on changing questions by a non-administrator."""
        resp = self.client.patch(reverse('question-list'))

        expected = b'{"detail":"Authentication credentials were not provided."}'
        self.assertEqual(resp.content, expected)

    def test_update_as_admin(self):
        """Change of questions by the administrator."""
        auth_headers = self.get_token()
        resp = self.client.patch(reverse('question-detail', kwargs={'pk': 5}), data=json.dumps({
            'type': 2
        }), content_type='application/json', **auth_headers)

        expected = b'{"id":5,"question":"What kind of animals do you like?","type":2,"questionnaire_id":4}'
        self.assertEqual(resp.content, expected)

    def test_update_active_survey(self):
        """Change the question of an active survey with administrator rights."""
        self.active_survey()

        auth_headers = self.get_token()
        resp = self.client.patch(reverse('question-detail', kwargs={'pk': 5}), data=json.dumps({
            'type': 2
        }), content_type='application/json', **auth_headers)

        expected = b'{"message":"After specifying the start date for the survey, ' \
                   b'you cannot change the questions."}'
        self.assertEqual(resp.content, expected)

    def test_destroy_is_not_admin(self):
        """Deleting a question not as an administrator."""
        resp = self.client.delete(reverse('question-detail', kwargs={'pk': 5}))

        expected = b'{"detail":"Authentication credentials were not provided."}'
        self.assertEqual(resp.content, expected)

    def test_destroy_as_admin(self):
        """Deleting a question as an administrator."""
        auth_headers = self.get_token()
        resp = self.client.delete(reverse('question-detail', kwargs={'pk': 5}),
                                  **auth_headers)
        self.assertEqual(resp.status_code, 204)

    def test_destroy_as_admin_active_survey(self):
        """Deleting an active survey question as administrator."""
        self.active_survey()

        auth_headers = self.get_token()
        resp = self.client.delete(reverse('question-detail', kwargs={'pk': 5}),
                                  **auth_headers)

        expected = b'{"message":"After specifying the start date of the survey, ' \
                   b'you cannot delete questions."}'
        self.assertEqual(resp.content, expected)

    def test_answers(self):
        """Checking the receipt of answer options for a question."""
        resp = self.client.get(reverse('question-answers', kwargs={'pk': 3}))

        expected = b'[{"id":1,"question_id":3,"text":"I like shoes."},' \
                  b'{"id":2,"question_id":3,"text":"I like shirt."}]'
        self.assertEqual(resp.content, expected)


class AnswerViewSetTest(TestCase):
    """
    Test fot view class AnswerViewSet
    """
    fixtures = ['initial_data.json']

    @classmethod
    def setUpTestData(cls):
        """Create superuser."""
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='12345678')

    @staticmethod
    def active_survey() -> None:
        """Setting active polling."""
        today = date.today()

        animals = Questionnaire.objects.get(id=4)
        animals.date_start = today
        animals.date_stop = today
        animals.save()

    def get_token(self):
        """Getting a token."""
        resp = self.client.post(reverse('user_login'), {
            'email': 'admin@gmail.com', 'password': '12345678'
        })

        token = resp.data['token']
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + token}

        return auth_headers

    def test_create_is_not_admin(self):
        """Check the prohibition of creating questions by a non-administrator."""
        resp = self.client.post(reverse('answer-list'))

        expected = b'{"detail":"Authentication credentials were not provided."}'
        self.assertEqual(resp.content, expected)

    def test_create_as_admin(self):
        """Creation of questions by the administrator."""
        auth_headers = self.get_token()
        resp = self.client.post(reverse('answer-list'), {
            'question_id': 3,
            'text': 'I like warm clothes.'
        }, **auth_headers)

        expected = b'{"id":6,"question_id":3,"text":"I like warm clothes."}'
        self.assertEqual(resp.content, expected)

    def test_create_wrong_type_of_question(self):
        """Creation of an answer to a question that requires a written answer."""
        auth_headers = self.get_token()
        resp = self.client.post(reverse('answer-list'), {
            'question_id': 1,
            'text': 'I like warm weather.'
        }, **auth_headers)

        expected = b'{"message":"This type of question requires a text answer."}'
        self.assertEqual(resp.content, expected)

    def test_create_active_survey(self):
        """Create a answer for an active survey with administrator rights."""
        self.active_survey()

        auth_headers = self.get_token()
        resp = self.client.post(reverse('answer-list'), {
            'question_id': 5,
            'text': 'I like dogs.'
        }, **auth_headers)

        expected = b'{"message":"After specifying the start date ' \
                   b'of the survey, you cannot create new answers."}'
        self.assertEqual(resp.content, expected)

    def test_create_without_question_id(self):
        """Creation of answer by the administrator without 'question_id'."""
        auth_headers = self.get_token()
        resp = self.client.post(reverse('answer-list'), {
            'text': 'I like warm clothes.'
        }, **auth_headers)

        expected = b'{"message":"No \'question_id\' specified."}'
        self.assertEqual(resp.content, expected)

    def test_update_is_not_admin(self):
        """Check the ban on changing answers by a non-administrator."""
        resp = self.client.patch(reverse('answer-list'))

        expected = b'{"detail":"Authentication credentials were not provided."}'
        self.assertEqual(resp.content, expected)

    def test_update_as_admin(self):
        """Change of answers by the administrator."""
        auth_headers = self.get_token()
        resp = self.client.patch(reverse('answer-detail', kwargs={'pk': 1}), data=json.dumps({
            'text': 'I like T-shirt'
        }), content_type='application/json', **auth_headers)

        expected = b'{"id":1,"question_id":3,"text":"I like T-shirt"}'
        self.assertEqual(resp.content, expected)

    def test_update_active_survey(self):
        """Change the answer of an active survey with administrator rights."""
        self.active_survey()

        auth_headers = self.get_token()
        resp = self.client.patch(reverse('answer-detail', kwargs={'pk': 5}), data=json.dumps({
            'text': 'I like T-shirt'
        }), content_type='application/json', **auth_headers)

        expected = b'{"message":"After specifying the start date for the survey, ' \
                   b'you cannot change the answers."}'
        self.assertEqual(resp.content, expected)

    def test_destroy_is_not_admin(self):
        """Deleting a answer not as an administrator."""
        resp = self.client.delete(reverse('answer-detail', kwargs={'pk': 5}))

        expected = b'{"detail":"Authentication credentials were not provided."}'
        self.assertEqual(resp.content, expected)

    def test_destroy_as_admin(self):
        """Deleting a answer as an administrator."""
        auth_headers = self.get_token()
        resp = self.client.delete(reverse('answer-detail', kwargs={'pk': 5}),
                                  **auth_headers)
        self.assertEqual(resp.status_code, 204)

    def test_destroy_as_admin_active_survey(self):
        """Deleting an active survey answer as administrator."""
        self.active_survey()

        auth_headers = self.get_token()
        resp = self.client.delete(reverse('answer-detail', kwargs={'pk': 5}),
                                  **auth_headers)

        expected = b'{"message":"After specifying the start date of the survey, ' \
                   b'you cannot delete answers."}'
        self.assertEqual(resp.content, expected)


class AnswerUserViewSetTest(TestCase):
    """Test fot view class AnswerUserViewSet"""
    fixtures = ['initial_data.json']

    def test_create(self):
        """Checking the creation of answers to questions of any user."""
        dataset = [
            {'user_id': 1, 'question': 2, 'text_answer': 'I like sunny weather.'},
            {'user_id': 1, 'text_answer': 'I like sunny weather.'},
            {'user_id': 1, 'question': 2, 'text_answer': 'I like sunny weather.'},
            {'user_id': 1, 'question': 3, 'text_answer': 'I like sunny weather.', 'choice_answer': 1},
            {'user_id': 1, 'question': 3, 'text_answer': 'I like sunny weather.'},
            {'user_id': 1, 'question': 6, 'choice_answer': 1},
            {'user_id': 1, 'question': 3, 'choice_answer': [1, 2]},
            {'user_id': 1, 'question': 6},
        ]

        expected_list = [
            b'{"id":2,"user_id":1,"question":2,"text_answer":"I like sunny weather.","choice_answer":[]}',
            b'{"message":"No \'question\' specified."}',
            b'{"message":"The user already has an answer to this question."}',
            b'{"message":"It is forbidden to answer simultaneously with the text and the choice of answers."}',
            b'{"message":"There should be no textual response."}',
            b'{"message":"The answer must be text."}',
            b'{"message":"This question requires only one answer option."}',
            b'{"message":"The question must be answered."}',
        ]

        for i, data in enumerate(dataset):
            resp = self.client.post(reverse('answer_user-list'), data=json.dumps(data),
                                    content_type='application/json')
            self.assertEqual(resp.content, expected_list[i])

    def test_get_user_responses(self):
        """Checking for user responses to survey questions."""
        expected = b'{"Weather questionnaire.":{"What kind of weather do you like?":["I like sunny weather."]}}'

        resp = self.client.get(reverse('get_user_responses', kwargs={'pk': 1}))
        self.assertEqual(resp.content, expected)
