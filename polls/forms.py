from django import forms
from django.db.models import fields
from django.core.exceptions import ValidationError
from django.utils import timezone

from datetime import datetime

from accounts.models import *
from .models import *


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
        queryset=Group.objects.all(),
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
            raise ValidationError("- время на выполнение теста должно быть больше нуля")
        return time_to_complete

    def clean_assess_2(self):
        assess_2 = self.cleaned_data.get('assess_2', None)
        if not assess_2:
            raise ValidationError("- введите количество баллов для оценки '2'")
        if assess_2 < 0:
            raise ValidationError("- баллы для оценки '2' должны быть положительные")
        return assess_2

    def clean_assess_3(self):
        assess_3 = self.cleaned_data.get('assess_3', None)
        if not assess_3:
            raise ValidationError("- введите количество баллов для оценки '3'")
        if assess_3 <= 0:
            raise ValidationError("- баллы для оценки '3' должны быть больше нуля")
        return assess_3

    def clean_assess_4(self):
        assess_4 = self.cleaned_data.get('assess_4', None)
        if not assess_4:
            raise ValidationError("- введите количество баллов для оценки '4'")
        if assess_4 <= 0:
            raise ValidationError("- баллы для оценки '4' должны быть больше нуля")
        return assess_4

    def clean_assess_5(self):
        assess_5 = self.cleaned_data.get('assess_5', None)
        if not assess_5:
            raise ValidationError("- введите количество баллов для оценки '5'")
        if assess_5 <= 0:
            raise ValidationError("- баллы для оценки '5' должны быть больше нуля")
        return assess_5

    def clean_poll_for_group(self):
        poll_for_group = self.cleaned_data.get('poll_for_group', None)
        if not poll_for_group:
            raise ValidationError("- выберите группы, для которых доступен тест")
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
                raise ValidationError("- оценка выше должна иметь больше баллов, чем нижестоящая")
        return self.cleaned_data