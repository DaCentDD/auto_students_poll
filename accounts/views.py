from django.contrib import auth
from django.db.models.lookups import FieldGetDbPrepValueIterableMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.utils import timezone

from .forms import LoginForm
from .models import *


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = None
        if form.is_valid():
            cd = form.cleaned_data
            user_obj = User.objects.get(username=cd['username'])
            #print(user_obj.block_to)
            if user_obj.attemps >= 5:
                user_obj.block_to = timezone.now() + timezone.timedelta(minutes=10)
                user_obj.attemps = 0
            if (user_obj.block_to is not None) and user_obj.block_to > timezone.now(): 
                block_to_date = (user_obj.block_to + timezone.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
                messages.error(request, f"Аккаунт заблокирован до {block_to_date} из-за большого количества попыток авторизации")
                user_obj.save()
                return render(request, 'accounts/login.html', {'form': form})
            user_obj.attemps +=1
            user = authenticate(
                request, 
                username=cd['username'], 
                password=cd['password']
                )
        if user is not None:
            user_obj.attemps = 0
            user_obj.save()
            login(request, user)
            if request.user.is_staff is True:
                return redirect('/admin_page')
            else:
                return redirect(f'/student_page/{request.user.id}')
        else:
            user_obj.save()
            messages.error(request, "Неверное имя пользователя или пароль")
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/login/')

    
