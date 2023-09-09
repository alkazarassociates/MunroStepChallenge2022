# Generated by Django 4.2.4 on 2023-09-09 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0016_profile_fundraising'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='fundraising',
        ),
        migrations.AddField(
            model_name='profile',
            name='justgiving',
            field=models.CharField(choices=[('NO', 'I do not have a personal JustGiving page for this challenge.'), ('YES', 'I have a personal JustGiving page I set up for this challenge.')], default='NO', max_length=3),
        ),
    ]
