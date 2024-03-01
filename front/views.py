from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 

from main import models
from . import serialiser

def create_result(id):
    quiz_taker = models.QuizTaker.objects.get(id=id)
    correct = 0
    incorrect = 0
    for object in models.Answer.objects.filter(taker=quiz_taker):
        if object.is_correct:
            correct +=1
        else:
            incorrect +=1

    models.Result.objects.create(
        taker=quiz_taker,
        correct_answers=correct,
        incorrect_answers=incorrect
    )

def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(
        quiz = quiz
    )
    context = {
        'quiz':quiz,
        'questions':questions
    }
    return render(request, 'front/quiz-detail.html', context)


def create_answers(request, code):
    quiz = models.Quiz.objects.get(code=code)
    full_name = request.POST['full_name']
    phone = request.POST['phone']
    email = request.POST.get('email')
    quiz_taker = models.QuizTaker.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        quiz=quiz
    )
    for key, value in request.POST.items():
        if key.isdigit():
            models.Answer.objects.create(
                taker=quiz_taker,
                question_id=int(key),
                answer_id=int(value)
            )
    create_result(quiz_taker.id)
    return HttpResponse('Javobingiz yozildi')


# @api_view(['GET'])
# def quiz_detail_api(request, id):
    # try:
    #     quiz = models.Quiz.objects.get(id=id)
    #     questions = models.Question.objects.filter(quiz=quiz)
    #     options = models.Option.objects.filter(question__in=questions)

    #     quiz_serializer = serialiser.QuizSerializer(quiz)
    #     questions_serializer = serialiser.QuestionSerializer(questions, many=True)
    #     options_serializer = serialiser.OptionSerializer(options, many=True)

    #     combined_data = {
    #         'quiz': quiz_serializer.data,
    #         'questions': questions_serializer.data,
    #         'options': options_serializer.data,
    #     }

    #     return Response(combined_data)
    # except models.Quiz.DoesNotExist:
    #     return Response({'error': 'Quiz not found'}, status=404)
    
@api_view(['GET'])
def quiz_detail_api(request, id):
    try:
        quiz = models.Quiz.objects.get(id=id)
    except models.Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

    quiz_serializer = serialiser.QuizSerializer(quiz)
    questions = models.Question.objects.filter(quiz=quiz)
    questions_serializer = serialiser.QuestionSerializer(questions, many=True)
    
    options_data = {}
    for question in questions:
        options = models.Option.objects.filter(question=question)
        options_serializer = serialiser.OptionSerializer(options, many=True)
        options_data[question.id] = options_serializer.data

    response_data = {
        'quiz': quiz_serializer.data,
        'questions': questions_serializer.data,
        'options': options_data,
    }

    return Response(response_data, status=status.HTTP_200_OK)

    
    