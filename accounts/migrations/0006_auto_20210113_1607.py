# Generated by Django 3.1.4 on 2021-01-13 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210108_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='attemps',
            field=models.IntegerField(default=0),
        ),
    ]