from django.http.response import Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


@login_required(login_url='/login')
def main(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    else:
        return redirect("/admin_page/")


@login_required(login_url='/login')
def student_page(request):
    return render(request, 'polls/student_page.html')


@login_required(login_url='/login')
def admin_page(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    return render(request, 'polls/admin_page.html')


@login_required(login_url='/login')
def poll_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        print(request.POST)
    form = PollForm()
    return render(request, 'polls/poll_create.html', {'form':form})