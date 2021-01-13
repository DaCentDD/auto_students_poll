from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.group_name


class User(AbstractUser):
    group_id = models.ForeignKey(
        'Group', 
        related_name='group_student', 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    attemps = models.IntegerField(default=0)
    block_to = models.DateTimeField(blank=True, null=True)


