# Generated by Django 3.2.14 on 2022-08-30 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0009_profile_team'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='stepentry',
            constraint=models.UniqueConstraint(fields=('peaker', 'date'), name='One Entry for day in September'),
        ),
    ]
