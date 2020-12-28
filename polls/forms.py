from django import forms
from django.db.models import fields


from accounts.models import *
from .models import *


class PollForm(forms.ModelForm):
    poll_name = forms.CharField(max_length=40, required=True)
    author_name = forms.CharField(max_length=40, required=True)
    active_from = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type': 'text', 'onfocus': "(this.type='date')", 'onblur':'this.type="text"'}))
    active_to = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type': 'text', 'onfocus': "(this.type='date')", 'onblur':'this.type="text"'}))
    max_attemps = forms.IntegerField(required=True)
    time_to_complete = forms.IntegerField(required=True)
    assess_2 = forms.IntegerField(required=True)
    assess_3 = forms.IntegerField(required=True)
    assess_4 = forms.IntegerField(required=True)
    assess_5 = forms.IntegerField(required=True)
    poll_for_group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

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
