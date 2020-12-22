from django.http.response import Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def main(request):
    return HttpResponse("Здесь будет проверяться админ ли")

@login_required(login_url='/login')
def student_page(request):
    return render(request, 'polls/student_page.html')

@login_required(login_url='/login')
def admin_page(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    return render(request, 'polls/admin_page.html')