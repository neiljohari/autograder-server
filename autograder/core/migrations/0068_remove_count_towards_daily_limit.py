# Generated by Django 3.0.5 on 2020-04-30 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_late_day_rework_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='count_towards_daily_limit',
        ),
    ]
