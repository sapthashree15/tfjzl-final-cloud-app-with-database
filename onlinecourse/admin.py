from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor

# <HINT> Register QuestionInline and ChoiceInline classes here
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# <HINT> Register Question and Choice models here


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
