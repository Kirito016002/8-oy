from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from main import models


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


@login_required
def quiz_list(request):
    try:
        data = models.Quiz.objects.all()
    except:
        data = 0
    context = {'data':data}
    return render(request, 'dashboard/quiz/index.html', context)

@login_required
def quiz_create(request, id):
    if request.method == 'POST':
        author = User.objects.get(id = id)
        models.Quiz.objects.create(
            author = author,
            title = request.POST['title']
        )
        return redirect('dashboard:quiz-list')
    return render(request, 'dashboard/quiz/create.html')
