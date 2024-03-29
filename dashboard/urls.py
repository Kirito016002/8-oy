from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    path('', views.main, name = 'main'),
    #quiz create
    path('create-quizz', views.create_quiz, name = 'quiz_create'),
    path('create-question/<int:id>', views.create_question , name ='quest_create' ),
    #quiz & questions detials
    path('questions/<int:id>', views.questions_list, name = 'questions'),
    path('start_or_breake/<int:id>', views.start_or_breake, name = 'start_or_breake'),
    path('question-detail/<int:id>', views.quest_detail, name = 'quest_detail'),
    path('quiz-delete/<int:id>', views.quiz_delete , name ='quiz_delete' ),
    path('get-results/<int:id>', views.get_results , name ='get_results' ),
    path('result-detail/<int:id>', views.result_detail , name ='result_detail' ),
    
    path('generate_excel/', views.generate_excel, name='generate_excel'),
]