from datetime import datetime
from django.db import models
from django.conf import settings
import django.utils.timezone


from collections import defaultdict


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

    class Meta:
        ordering = ('-active_from',)


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
    is_started = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def get_asses(self):
        if self.points <= self.poll_id.assess_2:
            self.assess = 2
        elif self.points <= self.poll_id.assess_3:
            self.assess = 3
        elif self.points <= self.poll_id.assess_4:
            self.assess = 4
        elif self.points <= self.poll_id.assess_5:
            self.assess = 5

    def check_result(self, data):
        answers = data.getlist('question_answer')
        self.points = 0
        if_question_correct, question_right_answers = defaultdict(bool), defaultdict(list)
        for answer in answers:   
            if not answer: 
                continue    
            answer_obj = Answer.objects.get(id=int(answer)) 
            if not if_question_correct.get(answer_obj.question_id.id, True): # Если для вопроса уже установлен флаг "неверно"
                continue
            if answer_obj.question_id.many_correct is True: # Если вопрос с множеством правильных ответов
                if not answer_obj.question_id.id in question_right_answers.keys(): # Если вопрос ещё не обрабатывался
                    question_right_answers[answer_obj.question_id.id] = \
                        [right_answer for right_answer in answer_obj.question_id.question_answer.all() if right_answer.is_right==True]  # Содаем список с правильными ответами 
                if answer_obj.is_right:  # Если текущий ответ правильный
                    if_question_correct[answer_obj.question_id.id] = True  # Устанавливаем для вопроса флаг верно  
                    question_right_answers[answer_obj.question_id.id].remove(answer_obj) # Удаляем ответ из списка правильных вопросов
                else:
                    if_question_correct[answer_obj.question_id.id] = False  # Если ответ неправильный, то весь вопрос считается не отвеченным
            else: # Если правильный ответ один, то добавляем баллов за вопрос
                if answer_obj.is_right:
                    self.points += answer_obj.question_id.points_for_question
        
        for question_id, is_right in if_question_correct.items(): # Проверяем результаты обработки вопросов с несколькими праввильными ответами
            if question_id in question_right_answers.keys(): # Проверяем на то, все ли правильные вопросы были выбраны
                if len(question_right_answers[question_id]) > 0: # Если какой-то правильный ответ не выбран, то баллов не даем
                    continue
            if is_right: # Иначе добавляем баллов
                self.points += Question.objects.get(id=question_id).points_for_question


        



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