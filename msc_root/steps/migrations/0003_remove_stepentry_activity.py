# Generated by Django 3.2.14 on 2022-08-16 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0002_remove_stepentry_steps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stepentry',
            name='activity',
        ),
    ]