# Generated by Django 3.1.3 on 2020-11-18 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire_api', '0003_auto_20201118_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ansewruser',
            name='text_answer',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
