from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from main import models
from . import funcs


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


#Quiz

@login_required
def quiz_list(request):
    try:
        data = models.Quiz.objects.filter(author=request.user)
    except:
        data = 0
    context = {'data':data}
    return render(request, 'dashboard/quiz/index.html', context)

@login_required
def quiz_create(request):
    if request.method == 'POST':
        models.Quiz.objects.create(
            author = request.user,
            title = request.POST['title']
        )
        return redirect('dashboard:quiz-list')
    return render(request, 'dashboard/quiz/create.html')


# Question

@login_required
def question_list(request, id):
    questions = models.Question.objects.filter(quiz_id = id)
    # options ={}
    # for quest in questions:
    #     option = models.Option.objects.get(question = quest, is_correct=True)
    #     new_data = {f'{quest}': option}
    #     options.update(new_data)
    context = {'questions':questions}
    return render(request, 'dashboard/question/index.html', context)


@login_required
def question_create(request):
    if request.method == 'POST':
        print(request)
        return redirect('dashboard:question-create')
    return render(request, 'dashboard/question/create.html')
