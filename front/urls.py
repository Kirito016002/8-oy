from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('quiz/<str:code>', views.quiz_detail, name='quiz_detail'),
    path('quiz-link-copy/<str:code>', views.quiz_link_copy, name='quiz_link_copy'),
    path('create-answer/<str:code>/', views.create_answers, name='create_answers'),
    path('quiz-detail-api/<int:id>', views.quiz_detail_api, name='quiz-detail-api'),
]