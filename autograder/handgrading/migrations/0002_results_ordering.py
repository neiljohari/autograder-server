# Generated by Django 2.0.1 on 2018-03-02 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handgrading', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('pk',)},
        ),
        migrations.AlterModelOptions(
            name='criterionresult',
            options={'ordering': ('criterion___order',)},
        ),
        migrations.AlterOrderWithRespectTo(
            name='annotation',
            order_with_respect_to='handgrading_rubric',
        ),
        migrations.AlterOrderWithRespectTo(
            name='criterion',
            order_with_respect_to='handgrading_rubric',
        ),
    ]
