# Generated by Django 3.1.3 on 2020-11-15 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire_api', '0002_auto_20201114_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='date_start',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='date_stop',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
