from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Count

from openpyxl import Workbook
import clipboard

from main import models
from . import funcs


@login_required
def main(request):
    try:
        quizes = models.Quiz.objects.filter(author = request.user)
        data = [
            {'label': 'Category 1', 'value': 20},
            {'label': 'Category 2', 'value': 30},
            {'label': 'Category 3', 'value': 50},
        ]
        context = {
            "quizes" : quizes,
            'chart_data': data
        }
        return render(request, 'dashboard/main.html', context)
    except:
        return render(request, 'dashboard/main.html')

@login_required
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST['title']
        time = request.POST['time']
        print(time)
        quiz = models.Quiz.objects.create(
            title = title,
            author = request.user,
            end_time = time
        )
        return redirect('dash:quest_create', quiz.id)
    return render(request, 'dashboard/quiz/create-quiz.html')

@login_required
def create_question(request, id):
    quiz = models.Quiz.objects.get(id = id)
    if request.method == 'POST':
        
        title = request.POST['title']
        ques = models.Question.objects.create(
            quiz = quiz,
            title = title
        )
        models.Option.objects.create(
            question = ques,
            name = request.POST['correct'],
            is_correct = True
        )
        data = [request.POST['incorrect1'], request.POST['incorrect2'], request.POST['incorrect3']]

        for i in data:
            models.Option.objects.create(
                question = ques,
                name = i,
            )
        if request.POST['submit_action'] == 'exit':
            return redirect('dash:main')

    return render (request, 'dashboard/quiz/create-question.html' )

@login_required
def start_or_breake(request, id):
    quiz = models.Quiz.objects.get(id = id)
    quiz.is_active = not quiz.is_active
    quiz.save()
    return redirect('dash:main')

@login_required
def questions_list(request, id):
    quests = models.Question.objects.filter(quiz_id = id)
    quiz = models.Quiz.objects.get(id = id)
    context = {
        'questions': quests,
        'quiz': quiz,
    }
    return render (request, 'dashboard/details/questions.html', context)

@login_required
def quest_detail(request, id):
    question = models.Question.objects.get(id = id)
    option_correct = models.Option.objects.get(question = question, is_correct = True)
    options = models.Option.objects.filter(question = question, is_correct = False).order_by('id')
    context = {
        'question': question,
        'options': options,
        'option_correct' : option_correct
    }
    if request.method == 'POST':
        question.title = request.POST['title']
        question.save()

        option_correct.name = request.POST['correct']
        option_correct.save()

        data = [request.POST['incorrect1'], request.POST['incorrect2'], request.POST['incorrect3']]

        for i, opt in enumerate(options):
            opt.name = data[i]
            opt.save()
    return render( request, 'dashboard/details/detail.html', context)

@login_required
def quiz_delete(request, id):
    models.Quiz.objects.get(id = id).delete()
    return redirect('dash:main')

@login_required
def get_results(request, id):
    quiz = models.Quiz.objects.get(id=id)
    taker = models.QuizTaker.objects.filter(quiz=quiz)

    # results = []
    # for i in taker:
    #     results.append(Result.objects.get(taker=i))
    
    results = tuple(
            map(
            lambda x : models.Result.objects.get(taker=x),
            taker
        )
    )
    return render(request, 'dashboard/quiz/results.html', {'results':results})

def result_detail(request, id):
    result = models.Result.objects.get(id=id)
    answers = models.Answer.objects.filter(taker=result.taker)
    context = {
        'taker':result.taker,
        'answers':answers
    }
    return render(request, 'dashboard/quiz/result-detail.html', context)


def generate_excel(request):
    wb = Workbook()
    ws = wb.active
    # res = models.Result.objects.annotate(num_questions=Count('question')).order_by('-num_questions')
    res = models.Result.objects.all()
    data = []
    for i in res:
        data.append(
            {
                'Full name':i.taker.full_name,
                'Phone':i.taker.phone,
                'Email':i.taker.email,
                'Questions':i.questions,
                'Correct answers':i.correct_answers,
                'Incorrect answers':i.incorrect_answers,
                'Percentage':i.percentage
            }
        )

    if data:
        headers = list(data[0].keys())
        ws.append(headers)
        for row in data:
            ws.append(list(row.values()))
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=example.xlsx'
    wb.save(response)

    return response
