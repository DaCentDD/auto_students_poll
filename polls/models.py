from datetime import datetime
from django.db import models
from django.conf import settings

class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    poll_name = models.CharField(max_length=40)
    author_name = models.CharField(max_length=40)
    poll_for_group = models.ManyToManyField(
        'accounts.Group', 
        related_name='group_for_poll',
        )
    active_from = models.DateTimeField(default=datetime.now)
    active_to = models.DateTimeField()
    max_attemps = models.IntegerField()
    time_to_complete = models.TimeField()
    #number_of_questions = models.IntegerField()
    assess_2 = models.IntegerField()
    assess_3 = models.IntegerField()
    assess_4 = models.IntegerField()
    assess_5 = models.IntegerField()

    class Meta:
        ordering = ('active_to',)


class PollResult(models.Model):
    username_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_poll'
    )
    poll_id = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='poll_result'
    )
    current_attemps = models.IntegerField(blank=True, null=True)
    points = models.IntegerField()
    time_spent = models.TimeField()
    assess = models.CharField(max_length=20)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    poll_id = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='poll_question'
    )
    question_text = models.CharField(max_length=100)
    points_for_question = models.IntegerField()
    many_correct = models.BooleanField(default=False)


class Answer(models.Model):
    question_id = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='question_answer'
    )
    answer_text = models.CharField(max_length=50)
    is_right = models.BooleanField(default=False)