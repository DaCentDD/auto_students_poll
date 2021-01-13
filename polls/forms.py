from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import *
from .models import *


class AnswersForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = [
            'answer_text',
            'question_id',
            'is_right',
        ]


class QuestionForm(forms.ModelForm):
    many_correct = forms.BooleanField(required=False)

    class Meta:
        model = Question
        fields = [
            'question_text',
            'points_for_question',
            'many_correct',
            'poll_id',
        ]


class PassQuestionForm(forms.ModelForm):
    question_text = forms.CharField(disabled=True, widget=forms.TextInput)
    points_for_question = forms.IntegerField(disabled=True)
    question_answer = forms.ModelChoiceField(queryset=Answer.objects.all(), widget=forms.Select(attrs={"class":"form-control", "size":"1"}), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")  
        if instance.many_correct is True:
            self.fields['question_answer'] = forms.ModelMultipleChoiceField(
                queryset=instance.question_answer.all(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
            )

        # else:
        #     self.fields['question_answer'] = forms.ModelChoiceField(
        #         queryset=instance.question_answer.all(),
        #         widget=forms.RadioSelect(attrs={'name':"check"}),
        #         required=False,
        #     )


    class Meta:
        model = Question
        fields = [
            'question_text',
            'points_for_question',
            'many_correct',
            'poll_id',
        ]


class ChangeGroupForm(forms.ModelForm):
    group_name = forms.CharField(max_length=8, required=False)
    group_student = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(is_staff=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = [
            'group_name',
            'group_student',
        ]


class PasswordStudentForm(forms.ModelForm):
    password = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput)
    repeat_password = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'password',
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        if not password:
            raise ValidationError("- введите пароль")
        return password

    def clean(self):
        repeat_password = self.cleaned_data.get("repeat_password", None)
        password = self.cleaned_data.get("password", None)
        if repeat_password != password:
            raise ValidationError("- пароли не совпадают")
        return self.cleaned_data


class ChangeStudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.CharField(
        max_length=254, required=False, widget=forms.EmailInput)
    group_id = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by("group_name"),
        widget=forms.RadioSelect,
        required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'group_id'
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", None)
        if not first_name:
            raise ValidationError("- введите имя студента")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", None)
        if not last_name:
            raise ValidationError("- введите фамилию студента")
        return last_name

    def clean_group_id(self):
        group_id = self.cleaned_data.get("group_id", None)
        if not group_id:
            raise ValidationError("- выберите учебную группу пользователя")
        return group_id


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, required=False)
    last_name = forms.CharField(max_length=15, required=False)
    username = forms.CharField(max_length=8, required=False)
    password = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput)
    repeat_password = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput)
    email = forms.CharField(
        max_length=254, required=False, widget=forms.EmailInput)
    group_id = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by("group_name"),
        widget=forms.RadioSelect,
        required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'group_id'
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username", None)
        if username:
            try:
                User.objects.get(username=username)
            except ObjectDoesNotExist:
                return username
            else:
                raise ValidationError(
                    "- пользователь с таким именем уже существует")
        else:
            raise ValidationError("- введите никнейм студента")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", None)
        if not first_name:
            raise ValidationError("- введите имя студента")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", None)
        if not last_name:
            raise ValidationError("- введите фамилию студента")
        return last_name

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        if not password:
            raise ValidationError("- введите пароль")
        return password

    def clean_group_id(self):
        group_id = self.cleaned_data.get("group_id", None)
        if not group_id:
            raise ValidationError("- выберите учебную группу пользователя")
        return group_id

    def clean(self):
        repeat_password = self.cleaned_data.get("repeat_password", None)
        password = self.cleaned_data.get("password", None)
        if repeat_password != password:
            raise ValidationError("- пароли не совпадают")
        return self.cleaned_data


class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=8, required=False)
    student_for_group = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().exclude(is_staff=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_group_name(self):
        group_name = self.cleaned_data.get("group_name", None)
        if group_name:
            try:
                Group.objects.get(group_name=group_name)
            except ObjectDoesNotExist:
                return group_name
            else:
                raise ValidationError("- такая группа уже существует")
        else:
            raise ValidationError("- введите название группы")


class PollForm(forms.ModelForm):
    poll_name = forms.CharField(max_length=40, required=False)
    author_name = forms.CharField(max_length=40, required=False)
    active_from = forms.DateTimeField(required=False, widget=forms.DateInput(
        attrs={'type': 'text', 'onfocus': "(this.type='date')", 'onblur': 'this.type="text"'}))
    active_to = forms.DateTimeField(required=False, widget=forms.DateInput(
        attrs={'type': 'text', 'onfocus': "(this.type='date')", 'onblur': 'this.type="text"'}))
    max_attemps = forms.IntegerField(required=False)
    time_to_complete = forms.IntegerField(required=False)
    assess_2 = forms.IntegerField(required=False)
    assess_3 = forms.IntegerField(required=False)
    assess_4 = forms.IntegerField(required=False)
    assess_5 = forms.IntegerField(required=False)
    poll_for_group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().order_by("group_name"),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Poll
        fields = [
            'poll_name',
            'author_name',
            'poll_for_group',
            'active_from',
            'active_to',
            'max_attemps',
            'time_to_complete',
            'assess_2',
            'assess_3',
            'assess_4',
            'assess_5',
        ]

    def clean_poll_name(self):
        poll_name = self.cleaned_data.get('poll_name', None)
        if poll_name:
            return poll_name
        else:
            raise ValidationError("- введите название теста")

    def clean_author_name(self):
        author_name = self.cleaned_data.get('author_name', None)
        if author_name:
            return author_name
        else:
            raise ValidationError("- введите имя автора")

    def clean_active_from(self):
        active_from = self.cleaned_data.get('active_from', None)
        if not active_from:
            active_from = timezone.now()
        if active_from < (timezone.now() - timezone.timedelta(days=1)):
            raise ValidationError(
                "- дата начала теста не может быть в прошлом")
        return active_from

    def clean_active_to(self):
        active_to = self.cleaned_data.get('active_to', None)
        active_from = self.cleaned_data.get('active_from', None)
        if not active_to:
            raise ValidationError("- выберите дату окончания тестирования")
        if active_from is not None:
            if active_to <= active_from:
                raise ValidationError(
                    "- дата окончания теста не может быть раньше или равна началу")
        return active_to

    def clean_max_attemps(self):
        max_attemps = self.cleaned_data.get('max_attemps', None)
        if not max_attemps:
            max_attemps = 1
        if max_attemps <= 0:
            raise ValidationError(
                "- количество попыток должно быть больше нуля")
        return max_attemps

    def clean_time_to_complete(self):
        time_to_complete = self.cleaned_data.get('time_to_complete', None)
        if not time_to_complete:
            raise ValidationError("- введите время на выполнение теста")
        if time_to_complete <= 0:
            raise ValidationError(
                "- время на выполнение теста должно быть больше нуля")
        return time_to_complete

    def clean_assess_2(self):
        assess_2 = self.cleaned_data.get('assess_2', None)
        if not assess_2 and (assess_2 != 0):
            raise ValidationError("- введите количество баллов для оценки '2'")
        if assess_2 < 0:
            raise ValidationError(
                "- баллы для оценки '2' должны быть положительные")
        return assess_2

    def clean_assess_3(self):
        assess_3 = self.cleaned_data.get('assess_3', None)
        if not assess_3 and (assess_3 != 0):
            raise ValidationError("- введите количество баллов для оценки '3'")
        if assess_3 <= 0:
            raise ValidationError(
                "- баллы для оценки '3' должны быть больше нуля")
        return assess_3

    def clean_assess_4(self):
        assess_4 = self.cleaned_data.get('assess_4', None)
        if not assess_4 and (assess_4 != 0):
            raise ValidationError("- введите количество баллов для оценки '4'")
        if assess_4 <= 0:
            raise ValidationError(
                "- баллы для оценки '4' должны быть больше нуля")
        return assess_4

    def clean_assess_5(self):
        assess_5 = self.cleaned_data.get('assess_5', None)
        if not assess_5 and (assess_5 != 0):
            raise ValidationError("- введите количество баллов для оценки '5'")
        if assess_5 <= 0:
            raise ValidationError(
                "- баллы для оценки '5' должны быть больше нуля")
        return assess_5

    def clean_poll_for_group(self):
        poll_for_group = self.cleaned_data.get('poll_for_group', None)
        if not poll_for_group:
            raise ValidationError(
                "- выберите группы, для которых доступен тест")
        return poll_for_group

    def clean(self):
        assess_2 = self.cleaned_data.get('assess_2', None)
        assess_3 = self.cleaned_data.get('assess_3', None)
        assess_4 = self.cleaned_data.get('assess_4', None)
        assess_5 = self.cleaned_data.get('assess_5', None)
        if None not in (assess_2, assess_3, assess_4, assess_5):
            if assess_2 <= assess_3 < assess_4 < assess_5:
                return self.cleaned_data
            else:
                raise ValidationError(
                    "- оценка выше должна иметь больше баллов, чем нижестоящая")
        return self.cleaned_data
