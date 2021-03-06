from django.db import models


class Questionnaire(models.Model):
    """This class contains polls."""
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_start = models.DateField(null=True, blank=True)
    date_stop = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-date_start']


class Question(models.Model):
    """This class contains questions for surveys."""
    TYPE_ANSWER = (
        (1, 'Text answer'),
        (2, 'One choice answer'),
        (3, 'Multiple choice answer')
    )
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question = models.TextField()
    type = models.IntegerField(choices=TYPE_ANSWER)

    def __str__(self):
        return self.question


class Answer(models.Model):
    """This class contains answers to questions."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class AnsewrUser(models.Model):
    """This class contains user answers to questions."""
    user_id = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.CharField(max_length=500, blank=True)
    choice_answer = models.ManyToManyField(Answer, blank=True)

    def __str__(self):
        if self.text_answer:
            return self.text_answer
        return f"{', '.join(map(str, self.choice_answer.all()))}"
