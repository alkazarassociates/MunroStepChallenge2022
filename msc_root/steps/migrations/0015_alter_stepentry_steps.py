# Generated by Django 3.2.14 on 2022-09-02 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0014_alter_profile_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepentry',
            name='steps',
            field=models.IntegerField(help_text="No ',' or '.' please. Just digits."),
        ),
    ]