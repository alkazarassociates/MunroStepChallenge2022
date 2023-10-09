# Generated by Django 4.2.4 on 2023-09-09 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0017_remove_profile_fundraising_profile_justgiving'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='justgiving',
            field=models.BooleanField(default=False, help_text='Check this if you have set up a personal JustGiving page for this challenge.', verbose_name='JustGiving'),
        ),
    ]