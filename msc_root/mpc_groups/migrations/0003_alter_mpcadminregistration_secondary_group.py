# Generated by Django 3.2.14 on 2022-08-05 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpc_groups', '0002_auto_20220804_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpcadminregistration',
            name='secondary_group',
            field=models.CharField(blank=True, max_length=60, verbose_name='Optional second group'),
        ),
    ]