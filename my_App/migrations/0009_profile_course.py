# Generated by Django 2.0.2 on 2020-01-06 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20200105_2011'),
        ('my_App', '0008_question_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.ManyToManyField(to='teacher.Course'),
        ),
    ]
