from django.http.response import Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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


def question_validation(all_poll_details):
    question_list = list(all_poll_details.keys())  # Список всех ключей для среза
    question_list = question_list[question_list.index('question_0'):]  # Срез ключей вопросов и ответов
    question_id = 0
    question_error_list = []
    for question in question_list:
        if question.startswith('question'):
            question_details = all_poll_details[question][0].split(',')
            for detail in range(len(question_details)):
                if not question_details[detail]:
                    question_error_list.append(
                        f"{question_id} вопрос содержит пустое необходимое значение в поле \
                        {'название' if detail == 0 else 'баллы'}"
                        )

@login_required(login_url='/login')
def poll_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        form = PollForm(request.POST)
        test_dict = {'poll_name': ['Математика'],
                     'author_name': ['Рома'],
                     'active_from': [''],
                     'active_to': ['2020-12-31'],
                     'max_attemps': [''],
                     'time_to_complete': ['30'],
                     'assess_2': ['2'],
                     'assess_3': ['3'],
                     'assess_4': ['4'],
                     'assess_5': ['5'],
                     'poll_for_group': ['1', '2'],

                     'question_0': ['Тут все ок,2'],
                     'answer_0': ['44,true'],
                     'answer_1': ['22,false'],

                     'question_1': ['Несколько правильных и пустой,2'],
                     'answer_2': ['а,true'],
                     'answer_3': ['б,false'],
                     'answer_4': ['в,true'],
                     'answer_5': [',false'],

                     'question_2': [',2'],
                     'answer_6': [',true'],
                     'answer_7': [',false'],

                     'question_3': [','],
                     'answer_8': [',false'],
                     'answer_9': [',false'],
                     }
        questions = question_validation(all_poll_details=test_dict)
        if form.is_valid():
            print(request.POST)
        else:
            return render(request, 'polls/poll_create.html', {'form': form})
    form = PollForm()
    return render(request, 'polls/poll_create.html', {'form': form})


@login_required(login_url='/login')
def groups_menu(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    groups = Group.objects.all().order_by("group_name")
    return render(request, 'polls/groups_menu.html', {'groups': groups})


@login_required(login_url='/login')
def group(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    group_obj = Group.objects.get(id=pk)
    if request.method == 'POST':
        form = ChangeGroupForm(request.POST, instance=group_obj)
        if form.is_valid():
            group_obj.group_name = form.cleaned_data["group_name"]
            group_obj.group_student.set(form.cleaned_data["group_student"])
            group_obj.save()
            
            return redirect("/groups/")  
    form = ChangeGroupForm(instance=group_obj)
    form.fields["group_student"].initial = User.objects.filter(group_id = group_obj.id)
    return render(request, 'polls/group.html', {'form': form, 'group':group_obj})
    


@login_required(login_url='/login')
def group_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            group_obj = Group.objects.create(group_name=cd["group_name"])
            print(cd)
            for student in cd["student_for_group"]:
                student_obj = User.objects.get(username=student)
                student_obj.group_id = group_obj
                student_obj.save()        
                return redirect("/groups/")   
        else:
            return render(request, 'polls/group_create.html', {'form': form} )
    form = CreateGroupForm()
    return render(request, 'polls/group_create.html', {'form': form})


@login_required(login_url='/login')
def student_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/students/")
        else:
            return render(request, 'polls/student_create.html', {'form': form})
    form = StudentForm()
    return render(request, 'polls/student_create.html', {'form': form})


@login_required(login_url='/login')
def students_menu(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    students = User.objects.exclude(is_staff=True)
    return render(request, 'polls/students_menu.html', {'students': students})


@login_required(login_url='/login')
def student(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    student_obj = User.objects.get(id=pk)
    if request.method == 'POST':
        form = ChangeStudentForm(request.POST, instance=student_obj)
        if form.is_valid():
            form.save()
            return redirect("/students/")  
    form = ChangeStudentForm(instance=student_obj)
    return render(request, 'polls/student.html', {'form': form, 'student':student_obj})


@login_required(login_url='/login')
def student_delete(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    User.objects.get(id=pk).delete()
    return redirect("/students/")


@login_required(login_url='/login')
def student_password(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    student_obj = User.objects.get(id=pk)
    if request.method == 'POST':
        form = PasswordStudentForm(request.POST, instance=student_obj)
        if form.is_valid():
            new_password = form.cleaned_data["password"]
            student_obj.set_password(new_password)
            student_obj.save()
            return redirect(f"/students/{pk}")
        else:
            print("INVALID")
            return render(request, 'polls/student_password.html', {'form': form, 'student': student_obj})
    form = PasswordStudentForm()   
    return render(request, 'polls/student_password.html', {'form': form, 'student': student_obj})