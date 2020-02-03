# Generated by Django 2.0.2 on 2020-01-04 21:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20200104_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='abbreviation',
            field=models.CharField(default=django.utils.timezone.now, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
