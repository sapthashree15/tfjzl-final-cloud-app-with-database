from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course

# <HINT> Register QuestionInline and ChoiceInline classes here
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


# <HINT> Register Question and Choice models here

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
