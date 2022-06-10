# Generated by Django 3.2.9 on 2021-11-30 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_software'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('metric_class', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionText', models.CharField(max_length=254)),
                ('questionAnswer', models.CharField(blank=True, max_length=254)),
                ('questionResult', models.CharField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareEvaluate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='softwareEvaluates2', to='main.evaluate')),
                ('software', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='softwareEvaluates', to='main.software')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rankValue', models.IntegerField(blank=True, max_length=20)),
                ('softwareEvaluate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ranks', to='main.softwareevaluate')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerValue', models.CharField(blank=True, max_length=256)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questionAnswers2', to='main.question')),
                ('softwareEvaluate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questionAnswers', to='main.softwareevaluate')),
            ],
        ),
        migrations.CreateModel(
            name='MetricValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metricValues', to='main.metric')),
                ('softwareEvaluate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='metricValues2', to='main.softwareevaluate')),
            ],
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compareResult', models.CharField(blank=True, max_length=256)),
                ('softwareEvaluate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='compares', to='main.softwareevaluate')),
                ('software_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='compares2', to='main.software')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.CharField(blank=True, max_length=1000)),
                ('softwareEvaluate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='main.softwareevaluate')),
            ],
        ),
    ]
