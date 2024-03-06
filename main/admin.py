from django.contrib import admin
from .models import Quiz, Question, Option, QuizTaker, Answer, Result

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizTaker)
admin.site.register(Answer)
admin.site.register(Result)
