# Generated by Django 3.1.4 on 2020-12-22 10:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20201221_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('poll_name', models.CharField(max_length=40)),
                ('author_name', models.CharField(max_length=40)),
                ('active_from', models.DateTimeField(default=datetime.datetime.now)),
                ('active_to', models.DateTimeField()),
                ('max_attemps', models.IntegerField()),
                ('time_to_complete', models.TimeField()),
                ('assess_2', models.IntegerField()),
                ('assess_3', models.IntegerField()),
                ('assess_4', models.IntegerField()),
                ('assess_5', models.IntegerField()),
                ('poll_for_group', models.ManyToManyField(related_name='group_for_poll', to='accounts.Group')),
            ],
            options={
                'ordering': ('active_to',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=100)),
                ('points_for_question', models.IntegerField()),
                ('many_correct', models.BooleanField(default=False)),
                ('poll_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_question', to='polls.poll')),
            ],
        ),
        migrations.CreateModel(
            name='PollResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_attemps', models.IntegerField(blank=True, null=True)),
                ('points', models.IntegerField()),
                ('time_spent', models.TimeField()),
                ('assess', models.CharField(max_length=20)),
                ('poll_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_result', to='polls.poll')),
                ('username_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_poll', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=50)),
                ('is_right', models.BooleanField(default=False)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='polls.question')),
            ],
        ),
    ]
