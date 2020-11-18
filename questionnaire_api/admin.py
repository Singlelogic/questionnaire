from django.contrib import admin

from .models import (
    Answer, AnsewrUser, Question, Questionnaire
)


admin.site.register(Answer)
admin.site.register(AnsewrUser)
admin.site.register(Question)
admin.site.register(Questionnaire)
