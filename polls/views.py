from collections import defaultdict
from typing import Protocol
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.functional import partition
from django.forms import formset_factory

from collections import defaultdict

from .forms import *
from .models import *


@login_required(login_url='/login')
def main(request):
    if request.user.is_staff is False:
        return redirect(f"/student_page/{request.user.id}")
    else:
        return redirect("/admin_page/")


@login_required(login_url='/login')
def student_page(request, pk):
    if int(pk) != request.user.id:
        return redirect(f"/student_page/{request.user.id}")
    polls = Poll.objects.filter(poll_for_group__id=request.user.group_id.id)
    return render(request, 'polls/student_page.html', {"polls": polls})


@login_required(login_url='/login')
def admin_page(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    return render(request, 'polls/admin_page.html')


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
    form.fields["group_student"].initial = User.objects.filter(
        group_id=group_obj.id)
    return render(request, 'polls/group.html', {'form': form, 'group': group_obj})


@login_required(login_url='/login')
def group_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            group_obj = Group.objects.create(group_name=cd["group_name"])
            for student in cd["student_for_group"]:
                student_obj = User.objects.get(username=student)
                student_obj.group_id = group_obj
                student_obj.save()
                return redirect("/groups/")
        else:
            return render(request, 'polls/group_create.html', {'form': form})
    form = CreateGroupForm()
    return render(request, 'polls/group_create.html', {'form': form})


@login_required(login_url='/login')
def group_delete(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    Group.objects.get(id=pk).delete()
    return redirect("/groups/")


@login_required(login_url='/login')
def student_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            user.set_password(password)
            user.save()
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
        else:
            return render(request, 'polls/student.html', {'form': form, 'student': student_obj})
    form = ChangeStudentForm(instance=student_obj)
    return render(request, 'polls/student.html', {'form': form, 'student': student_obj})


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
            return redirect(f"/students/student/{pk}")
        else:
            return render(request, 'polls/student_password.html', {'form': form, 'student': student_obj})
    form = PasswordStudentForm()
    return render(request, 'polls/student_password.html', {'form': form, 'student': student_obj})


# Проверка вопросов и ответов из POST
def question_validation(all_poll_details: dict):
    question_id, right_answer_count = 0, 0
    error_list, questions_and_answers = [], {
        'questions': [], 'answers': []}
    # Список всех ключей для среза
    question_answer_list = list(all_poll_details.keys())
    try:
        question_answer_list = question_answer_list[question_answer_list.index(
            'question_0'):]  # Срез ключей вопросов и ответов
    except ValueError:
        error_list.append("- добавьте хотя бы один вопрос")
        return error_list
    try:
        # Удаляю из выборки csrf токен
        question_answer_list.remove('csrfmiddlewaretoken')
    except ValueError:
        pass

    def check(element_type: str):  # Замыкание
        nonlocal right_answer_count
        for detail in range(len(element_details)):  # Проверка на валидность вопроса
            if not element_details[detail]:  # Если есть пустое значение
                if element_type == 'question':  # Ошибка вопроса
                    error_list.append(
                        f"- {question_id} вопрос содержит пустое необходимое значение в поле {'название' if detail == 0 else 'баллы'}"
                    )
                if element_type == 'answer':  # Ошибка ответа
                    error_list.append(
                        f"- ответ в {question_id} вопросе содержит пустое необходимое значение в поле {'текст ответа' if detail == 0 else 'правильный ответ'}"
                    )
            if element_type == 'question':
                if detail == 0:  # Добавляем в форму ответа сам вопрос
                    form.question_text = element_details[detail]
                if detail == 1:  # Либо баллы за вопрос
                    form.points_for_question = element_details[detail]
            if element_type == 'answer':
                if detail == 0:  # Добавляем в форму текст ответа
                    form.answer_text = element_details[detail]
                if detail == 1:  # И указываем правильный  ли ответ
                    form.is_right = True if element_details[detail] == 'true' else False
                    if form.is_right:
                        right_answer_count += 1              
            # Добавляем временное значение id вопроса в форму ответа
            form.question_id = question_id

    for element in question_answer_list:
        if element.startswith('question'): # Если вопрос
            print(right_answer_count)
            if right_answer_count < 1 and question_id > 0:  # Если нет хотя бы одного правильного ответа у вопроса
                error_list.append(
                    f"- {question_id} вопрос не содержит правильных ответов")
            elif right_answer_count > 1:  # Если правильных ответов больше одного
                questions_and_answers["questions"][question_id - 1].many_correct = True
            elif right_answer_count == 1:
                questions_and_answers["questions"][question_id - 1].many_correct = False
            question_id += 1
            right_answer_count = 0
            element_details = all_poll_details[element].split(',')
            form = QuestionForm()
            check('question')
            questions_and_answers['questions'].append(form)
        else:  # Если ответ
            element_details = all_poll_details[element].split(',')
            form = AnswersForm()
            check('answer')
            questions_and_answers['answers'].append(form)
            if element == question_answer_list[-1]: # Если последний элемент
                if right_answer_count < 1 and question_id > 0:  # Если нет хотя бы одного правильного ответа у вопроса
                    error_list.append(
                        f"- {question_id} вопрос не содержит правильных ответов")
                elif right_answer_count > 1:  # Если правильных ответов больше одного
                    questions_and_answers["questions"][question_id - 1].many_correct = True
                elif right_answer_count == 1:
                    questions_and_answers["questions"][question_id - 1].many_correct = False
    if len(error_list) > 0:
        return error_list
    else:
        return questions_and_answers


@login_required(login_url='/login')
def poll_create(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    if request.method == 'POST':
        form = PollForm(request.POST)
        questions_and_answers = question_validation(request.POST)
        if type(questions_and_answers) is list:  # Если после валидации вернулся список ошибок
            return render(request, 'polls/poll_create.html', {'form': form, 'q_and_a_errors': questions_and_answers})
        if form.is_valid():
            new_test = form.save()
            qst_id = 1  # Инициализация значения id вопроса для поиска нужных ответов
            for qst_form in questions_and_answers["questions"]:
                new_question = qst_form.save(commit=False)
                new_question.poll_id = new_test
                new_question.points_for_question = qst_form.points_for_question
                new_question.question_text = qst_form.question_text
                new_question.many_correct = qst_form.many_correct
                new_question.save()
                for ans_form in questions_and_answers["answers"]:
                    if ans_form.question_id == qst_id:
                        new_answer = ans_form.save(commit=False)
                        new_answer.question_id = new_question
                        new_answer.answer_text = ans_form.answer_text
                        new_answer.is_right = ans_form.is_right
                        new_answer.save()
                qst_id += 1
        else:
            return render(request, 'polls/poll_create.html', {'form': form})
    form = PollForm()
    return render(request, 'polls/poll_create.html', {'form': form})


@login_required(login_url='/login')
def polls_menu(request):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    polls_obj = Poll.objects.all().order_by("-active_from")
    return render(request, 'polls/polls_menu.html', {'polls_obj': polls_obj})


@login_required(login_url='/login')
def poll(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    poll_obj = Poll.objects.get(id=pk)
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll_obj)
        if form.is_valid():
            form.save()
            return redirect("/polls/")
        else:
            return render(request, 'polls/poll.html', {'form': form, 'poll': poll_obj})
    form = PollForm(instance=poll_obj)
    return render(request, 'polls/poll.html', {'form': form, 'poll': poll_obj})


@login_required(login_url='/login')
def poll_delete(request, pk):
    if request.user.is_staff is False:
        return redirect("/student_page/")
    Poll.objects.get(id=pk).delete()
    return redirect("/polls/")


@login_required(login_url='/login')
def poll_enter(request, pk, id):
    if int(pk) != request.user.id:
        return redirect(f"/student_page/{request.user.id}")
    current_poll = Poll.objects.get(id=id)
    questions = []
    if request.method == 'POST':
        new_result = PollResult(username_id=User.objects.get(id=int(pk)), poll_id=Poll.objects.get(id=int(id)), points=0)
        answers = request.POST.getlist('question_answer')
        if_question_correct = defaultdict(bool)
        for answer in answers:       
            answer_obj = Answer.objects.get(id=int(answer))
            if not if_question_correct.get(answer_obj.question_id.id, True):
                continue
            if answer_obj.question_id.many_correct is True:
                if answer_obj.is_right:
                    if_question_correct[answer_obj.question_id.id] = True
                else:
                    if_question_correct[answer_obj.question_id.id] = False        
            else:
                if answer_obj.is_right:
                    new_result.points += answer_obj.question_id.points_for_question
        print(if_question_correct)
        
    for question in current_poll.poll_question.all():
        form = PassQuestionForm(instance=question)
        form.fields['question_answer'].queryset = question.question_answer.all()
        questions.append(form)
    
    return render(request, 'polls/poll_pass.html', {'questions': questions, 'poll': current_poll})
