# Generated by Django 2.0.2 on 2020-01-08 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_App', '0010_submission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='input_cases',
        ),
        migrations.RemoveField(
            model_name='question',
            name='output_cases',
        ),
    ]
