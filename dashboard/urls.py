from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz-list', views.quiz_list, name='quiz-list'),
    path('quiz-create', views.quiz_create, name='quiz-create'),
    # question
    path('question-list/<int:id>', views.question_list, name='question-list'),
    path('question-create', views.question_create, name='question-create'),
]