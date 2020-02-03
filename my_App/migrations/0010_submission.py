# Generated by Django 2.0.2 on 2020-01-07 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_App', '0009_profile_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_submission', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_App.Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_App.Profile')),
            ],
        ),
    ]
