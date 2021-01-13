from datetime import datetime
from django.db import models
from django.conf import settings
import django.utils.timezone


class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    poll_name = models.CharField(max_length=40)
    author_name = models.CharField(max_length=40)
    poll_for_group = models.ManyToManyField(
        'accounts.Group', 
        related_name='group_for_poll',
        )
    active_from = models.DateTimeField(default=django.utils.timezone.now)
    active_to = models.DateTimeField()
    max_attemps = models.PositiveIntegerField(default=1)
    time_to_complete = models.PositiveIntegerField()
    assess_2 = models.PositiveIntegerField()
    assess_3 = models.PositiveIntegerField()
    assess_4 = models.PositiveIntegerField()
    assess_5 = models.PositiveIntegerField()
    is_started = models.BooleanField(default=False)

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
    assess = models.CharField(max_length=20)

    def get_asses(self):
        if self.points <= self.poll_id.assess_2:
            self.assess = 2
        elif self.points <= self.poll_id.assess_3:
            self.assess = 3
        elif self.points <= self.poll_id.assess_4:
            self.assess = 4
        elif self.points <= self.poll_id.assess_5:
            self.assess = 5

        



class Question(models.Model):
    id = models.AutoField(primary_key=True)
    poll_id = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='poll_question'
    )
    question_text = models.CharField(max_length=100)
    points_for_question = models.PositiveIntegerField()
    many_correct = models.BooleanField(default=False)


class Answer(models.Model):
    question_id = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='question_answer'
    )
    answer_text = models.CharField(max_length=50)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text