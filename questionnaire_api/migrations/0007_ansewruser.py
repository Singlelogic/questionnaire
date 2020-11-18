# Generated by Django 3.1.3 on 2020-11-18 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire_api', '0006_delete_ansewruser'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsewrUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('text_answer', models.CharField(blank=True, max_length=500)),
                ('choice_answer', models.ManyToManyField(blank=True, to='questionnaire_api.Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_api.question')),
            ],
        ),
    ]