# Generated by Django 3.2.9 on 2021-12-16 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_rename_question_questionevaluate_select_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionevaluate',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questionevaluate',
            name='select_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questionAnswers2', to='main.category'),
        ),
    ]
