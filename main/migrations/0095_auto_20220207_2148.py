# Generated by Django 3.2.9 on 2022-02-07 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricevaluate',
            name='evaluated_by',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='metricevaluate',
            name='isEvaluated',
            field=models.BooleanField(default=False),
        ),
    ]
