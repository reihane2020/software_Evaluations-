# Generated by Django 3.2.9 on 2021-12-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_rename_people_softwareevaluate_thepeople'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='softwareevaluate',
            name='thepeople',
        ),
        migrations.AddField(
            model_name='softwareevaluate',
            name='people',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
