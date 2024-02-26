from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz-list', views.quiz_list, name='quiz-list'),
    path('quiz-create/<int:id>', views.quiz_create, name='quiz-create'),
]