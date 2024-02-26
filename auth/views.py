from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def sign_up(request):
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         messages.success(request, f'Account created for {user.username}!')
    #         return redirect('dashboard:index')
    # else:
    #     form = UserCreationForm()
    
    
    if request.method == 'POST':        
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']    
        if password == password_confirm:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('dashboard:index')
        else:
            return HttpResponse('Parollar mos kelmadi')
    return render(request, 'dashboard/auth/sign_up.html')



def sign_in(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')
    return render(request, 'dashboard/auth/sign_in.html')


@login_required
def sign_out(request):
    logout(request)
    return redirect('auth:sign-in')