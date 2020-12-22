from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = None
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, 
                username=cd['username'], 
                password=cd['password']
                )
        if user is not None:
            login(request, user)
            if request.user.is_staff is True:
                return redirect('/admin_page')
            else:
                return redirect('/student_page')
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/login/')

    
