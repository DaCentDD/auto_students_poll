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
